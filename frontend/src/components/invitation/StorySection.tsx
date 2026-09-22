import type { InvitationData } from "./types";

export function StorySection({ data }: { data: InvitationData }) {
  return (
    <section className="invitation-section story-section" aria-labelledby="story-title">
      <div className="story-image" role="img" aria-label="A candid moment together" />
      <div className="story-copy">
        <p className="section-label">A little backstory</p>
        <h2 id="story-title">{data.story.title}</h2>
        <p>{data.story.body}</p>
      </div>
    </section>
  );
}
