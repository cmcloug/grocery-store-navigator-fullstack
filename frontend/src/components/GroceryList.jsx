import { useState } from "react";

function GroceryList({ items, onChange }) {
  const [text, setText] = useState("");

  function add(e) {
    e.preventDefault();
    // Allow pasting several items separated by commas or new lines.
    const added = text
      .split(/[,\n]/)
      .map((s) => s.trim())
      .filter((s) => s && !items.some((i) => i.toLowerCase() === s.toLowerCase()));
    if (added.length) onChange([...items, ...added]);
    setText("");
  }

  return (
    <div>
      <form className="row" onSubmit={add}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add an item (e.g. milk, eggs)"
          aria-label="Grocery item"
        />
        <button type="submit">Add</button>
      </form>
      <ul className="chips">
        {items.map((item) => (
          <li key={item}>
            {item}
            <button
              className="chip-remove"
              aria-label={`Remove ${item}`}
              onClick={() => onChange(items.filter((i) => i !== item))}
            >
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GroceryList;
