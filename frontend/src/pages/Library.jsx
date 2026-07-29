// frontend/src/pages/Library.jsx

import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { algorithmsApi } from "../api/algorithmsApi";
import Spinner from "../components/ui/Spinner";
import { CATEGORY_LABELS, CATEGORY_DESCRIPTIONS } from "../constants/categories";

export default function Library() {
  const { category } = useParams();


  const { data: allItems, isLoading } = useQuery({
    queryKey: ["library", "all"],
    queryFn: algorithmsApi.listAllForLibrary,
  });

  const filtered = allItems?.filter((a) => a.category === category) || [];



  const label = CATEGORY_LABELS[category] || "Unknown Category";
  const description = CATEGORY_DESCRIPTIONS[category];
  // const filtered = algorithms?.filter((a) => a.category === category) || [];

  return (
    <div className="p-8">
      <div className="max-w-5xl mx-auto flex flex-col gap-6">
        <div>
          <h1 className="text-2xl font-semibold text-ink">{label}</h1>
          {description && <p className="text-muted text-sm mt-1">{description}</p>}
        </div>

        {isLoading ? (
          <Spinner size="md" />
        ) : filtered.length === 0 ? (
          <div className="bg-surface border border-line rounded-xl p-8 text-center">
            <p className="text-muted text-sm">No algorithms in this category yet — check back soon.</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">

            {filtered.map((item) => {
              const dest = item.is_inference ? item.link_to : `/studio?algorithm=${item.name}`;
              const actionLabel = item.is_inference ? "Open →" : "Try in Studio →";
              return (
                <Link
                  key={item.name}
                  to={dest}
                  className="text-left p-4 rounded-xl border border-line bg-surface
                  hover:border-ink/20 hover:bg-surface-hover transition-colors cursor-pointer block"
                   >
                  <p className="font-medium text-ink">{item.display_name}</p>
                  <p className="text-xs text-faint mt-1 uppercase tracking-wide">
                    {item.is_inference ? "transformer · inference" : item.task_type}
                  </p>
                  <p className="text-xs text-muted mt-2 line-clamp-2">{item.description}</p>
                  <p className="text-xs text-ink mt-3 font-medium">{actionLabel}</p>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}