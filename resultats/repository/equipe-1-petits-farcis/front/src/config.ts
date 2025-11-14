const config = {
  useMockData: true, // Set to true to use mock data instead of backend API calls
  backend: {
    journeys: {
      baseUrl: "http://localhost:5000/api",
    },
    puzzle: {
      baseUrl: "http://localhost:5000/api/puzzle",
    },
  },
};

export default config;
