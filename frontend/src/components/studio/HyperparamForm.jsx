// frontend/src/components/studio/HyperparamForm.jsx

import { useState, useEffect } from "react";
import ParamInput from "./ParamInput";

export default function HyperparamForm({ algorithm, onChange }) {
  // Build initial state from each param's `default` value
  const [values, setValues] = useState({});

  useEffect(() => {
    if (!algorithm) return;
    const defaults = {};
    algorithm.parameters.forEach((p) => {
      defaults[p.name] = p.default;
    });
    setValues(defaults);
    onChange(defaults);
  }, [algorithm?.name]); // reset when algorithm changes

  const handleParamChange = (name, value) => {
    const updated = { ...values, [name]: value };
    setValues(updated);
    onChange(updated);
  };

  if (!algorithm || algorithm.parameters.length === 0) {
    return <p className="text-sm text-gray-400">No hyperparameters to configure.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      {algorithm.parameters.map((paramDef) => (
        <ParamInput
          key={paramDef.name}
          paramDef={paramDef}
          value={values[paramDef.name]}
          onChange={handleParamChange}
        />
      ))}
    </div>
  );
}