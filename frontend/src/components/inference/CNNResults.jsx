// frontend/src/components/inference/CNNResults.jsx

export default function CNNResults({ output }) {
  if (!output) return null;

  const {
    predicted_label,
    confidence,
    probabilities,
    class_names,
    image_base64,
  } = output;

  return (
    <div className="flex flex-col gap-5">

      {/* Uploaded image preview */}
      {image_base64 && (
        <div className="flex justify-center">
          <img
            src={`data:image/jpeg;base64,${image_base64}`}
            alt="Uploaded"
            className="max-h-48 rounded-xl border border-line object-cover"
          />
        </div>
      )}

      {/* Prediction */}
      <div className="text-center">
        <p className="text-[11px] text-faint uppercase tracking-wide mb-1">Prediction</p>
        <p className="text-3xl font-semibold text-ink capitalize">{predicted_label}</p>
        <p className="text-sm text-muted font-mono mt-1">{confidence}% confidence</p>
      </div>

      {/* Probability bars for each class */}
      <div className="flex flex-col gap-3">
        {class_names.map((cls) => {
          const prob = probabilities[cls] ?? 0;
          const isWinner = cls === predicted_label;
          return (
            <div key={cls}>
              <div className="flex justify-between text-xs mb-1">
                <span className={`capitalize font-medium ${isWinner ? "text-ink" : "text-muted"}`}>
                  {cls}
                </span>
                <span className="font-mono text-muted">{prob}%</span>
              </div>
              <div className="h-1.5 bg-line rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${isWinner ? "bg-ink" : "bg-muted"}`}
                  style={{ width: `${prob}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}