const config = {
  useMockData: true, // Set to true to use mock data instead of backend API calls
  backend: {
    journeys: {
      baseUrl: "https://01f3505f8752.ngrok-free.app/api",
    },
    puzzle: {
      baseUrl: "http://localhost:5000/api/puzzle",
    },
  },
};

export default config;
