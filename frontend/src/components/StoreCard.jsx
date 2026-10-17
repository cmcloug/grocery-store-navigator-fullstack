function StoreCard({ store, selected, onSelect }) {
  return (
    <div className={`store-card${selected ? " selected" : ""}`}>
      <div className="store-info">
        <h3>{store.name}</h3>
        <p>
          {store.address}, {store.city}
        </p>
      </div>
      <button onClick={() => onSelect(store)} disabled={selected}>
        {selected ? "Selected" : "Select Store"}
      </button>
    </div>
  );
}

export default StoreCard;
