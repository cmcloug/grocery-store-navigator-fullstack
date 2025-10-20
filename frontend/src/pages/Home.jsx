import StoreCard from "../components/StoreCard";

function Home() {
  const stores = [
    { id: 1, name: "Kroger", location: "Avon" },
    { id: 2, name: "Kroger", location: "Danville" },
    { id: 3, name: "Kroger", location: "Plainfield" },
    { id: 4, name: "Kroger", location: "Brownsburg" },
  ];

  return (
    <div className="home">
      <div className="stores-grid">
        {stores.map((store) => (
          <StoreCard store={store} key={store.id} />
        ))}
      </div>
    </div>
  );
}

export default Home;
