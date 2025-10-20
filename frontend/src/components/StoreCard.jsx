function StoreCard({ store }) {
  function onSelectClick() {
    alert("clicked");
  }

  return (
    <div className="store-card">
      <div className="store-overlay">
        <button className="select-btn" onClick={onSelectClick}>
          Select Store
        </button>
      </div>
      <div className="store-info">
        <h3>{store.name}</h3>
        <p>{store.location}</p>
      </div>
    </div>
  );
}

export default StoreCard;
