// Package storage wraps object storage (MinIO/S3-compatible) for media
// uploads.
package storage

import (
	"context"
	"fmt"
	"io"
	"net/url"
	"strings"

	"yukakad/internal/config"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

type Client struct {
	mc            *minio.Client
	bucket        string
	publicBaseURL string
}

func New(cfg config.Config) (*Client, error) {
	mc, err := minio.New(cfg.MinioEndpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(cfg.MinioAccessKey, cfg.MinioSecretKey, ""),
		Secure: cfg.MinioUseSSL,
	})
	if err != nil {
		return nil, fmt.Errorf("create minio client: %w", err)
	}

	ctx := context.Background()
	exists, err := mc.BucketExists(ctx, cfg.MinioBucket)
	if err != nil {
		return nil, fmt.Errorf("check bucket: %w", err)
	}
	if !exists {
		if err := mc.MakeBucket(ctx, cfg.MinioBucket, minio.MakeBucketOptions{}); err != nil {
			return nil, fmt.Errorf("create bucket: %w", err)
		}
	}
	// Uploaded media (gallery photos, QRIS images) is served directly to
	// public invitation visitors, so the bucket needs anonymous read.
	policy := fmt.Sprintf(`{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::%s/*"]}]}`, cfg.MinioBucket)
	_ = mc.SetBucketPolicy(ctx, cfg.MinioBucket, policy)

	publicBaseURL := cfg.MinioPublicBaseURL
	if publicBaseURL == "" {
		scheme := "http"
		if cfg.MinioUseSSL {
			scheme = "https"
		}
		publicBaseURL = fmt.Sprintf("%s://%s/%s", scheme, cfg.MinioEndpoint, cfg.MinioBucket)
	}

	return &Client{mc: mc, bucket: cfg.MinioBucket, publicBaseURL: strings.TrimSuffix(publicBaseURL, "/")}, nil
}

func (c *Client) Upload(ctx context.Context, key string, r io.Reader, size int64, contentType string) (string, error) {
	if _, err := c.mc.PutObject(ctx, c.bucket, key, r, size, minio.PutObjectOptions{ContentType: contentType}); err != nil {
		return "", fmt.Errorf("upload object: %w", err)
	}
	return c.publicBaseURL + "/" + key, nil
}

func (c *Client) DeleteURL(ctx context.Context, publicURL string) error {
	base, err := url.Parse(c.publicBaseURL)
	if err != nil {
		return fmt.Errorf("parse configured object URL: %w", err)
	}
	parsed, err := url.Parse(publicURL)
	if err != nil || parsed.Scheme != base.Scheme || parsed.Host != base.Host {
		return fmt.Errorf("object URL does not belong to configured bucket")
	}
	basePath := strings.TrimSuffix(base.Path, "/")
	key := strings.TrimPrefix(parsed.Path, basePath+"/")
	if key == "" {
		return fmt.Errorf("object key is empty")
	}
	if err := c.mc.RemoveObject(ctx, c.bucket, key, minio.RemoveObjectOptions{}); err != nil {
		return fmt.Errorf("delete object: %w", err)
	}
	return nil
}
