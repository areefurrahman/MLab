// frontend/src/components/inference/NERResults.jsx

const ENTITY_STYLES = {
  PER:  "border-b-2 border-ink",
  ORG:  "bg-surface-hover rounded px-0.5",
  LOC:  "italic underline underline-offset-2",
  MISC: "border border-line rounded px-0.5",
};

const ENTITY_LABELS = {
  PER: "Person",
  ORG: "Organization",
  LOC: "Location",
  MISC: "Misc",
};

export default function NERResults({ output }) {
  if (!output) return null;
  const { original_text, entities, entity_type_counts } = output;

  // Build annotated spans from character offsets
  const spans = buildSpans(original_text, entities);

  return (
    <div className="flex flex-col gap-5">
      <div className="bg-canvas border border-line rounded-lg p-4 leading-8 text-ink text-sm">
        {spans.map((span, i) =>
          span.entity ? (
            <span key={i} className={`relative ${ENTITY_STYLES[span.entity_type] || ""}`}>
              {span.text}
              <span className="absolute -top-4 left-0 text-[9px] text-faint uppercase tracking-wide">
                {span.entity_type}
              </span>
            </span>
          ) : (
            <span key={i}>{span.text}</span>
          )
        )}
      </div>

      <div className="flex flex-wrap gap-3">
        {Object.entries(entity_type_counts).map(([type, count]) => (
          <div key={type} className="bg-surface border border-line rounded-lg px-3 py-2">
            <p className="text-[11px] text-faint uppercase tracking-wide">{ENTITY_LABELS[type] || type}</p>
            <p className="text-lg font-mono font-semibold text-ink">{count}</p>
          </div>
        ))}
      </div>

      <p className="text-xs text-faint font-mono">{output.entity_count} entities found</p>
    </div>
  );
}

function buildSpans(text, entities) {
  if (!entities || entities.length === 0) return [{ text, entity: false }];

  const spans = [];
  let cursor = 0;

  for (const entity of entities) {
    if (entity.start > cursor) {
      spans.push({ text: text.slice(cursor, entity.start), entity: false });
    }
    spans.push({ text: entity.text, entity: true, entity_type: entity.entity_type });
    cursor = entity.end;
  }
  if (cursor < text.length) {
    spans.push({ text: text.slice(cursor), entity: false });
  }
  return spans;
}