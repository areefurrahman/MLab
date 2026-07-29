// frontend/src/components/studio/RulesTable.jsx

export default function RulesTable({ result }) {
  const rules = result?.rules || [];

  if (rules.length === 0) {
    return <p className="text-sm text-faint">No rules found at this threshold — try lowering min support/confidence.</p>;
  }

  return (
    <div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm font-mono">
          <thead>
            <tr className="border-b border-line">
              <th className="text-left px-3 py-2 text-faint font-sans uppercase text-xs tracking-wide">If you buy</th>
              <th className="text-left px-3 py-2 text-faint font-sans uppercase text-xs tracking-wide">Then likely</th>
              <th className="text-right px-3 py-2 text-faint font-sans uppercase text-xs tracking-wide">Support</th>
              <th className="text-right px-3 py-2 text-faint font-sans uppercase text-xs tracking-wide">Confidence</th>
              <th className="text-right px-3 py-2 text-faint font-sans uppercase text-xs tracking-wide">Lift</th>
            </tr>
          </thead>
          <tbody>
            {rules.map((rule, i) => (
              <tr key={i} className="border-b border-line last:border-0">
                <td className="px-3 py-2 text-ink">{rule.antecedents.join(", ")}</td>
                <td className="px-3 py-2 text-ink">{rule.consequents.join(", ")}</td>
                <td className="px-3 py-2 text-right text-muted">{rule.support}</td>
                <td className="px-3 py-2 text-right text-muted">{rule.confidence}</td>
                <td className="px-3 py-2 text-right text-ink font-semibold">{rule.lift}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-faint font-mono mt-3">
        {result.rule_count} rules · {result.transaction_count} transactions · {result.unique_items} unique items
      </p>
    </div>
  );
}