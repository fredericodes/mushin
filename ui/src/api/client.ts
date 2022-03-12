import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:10000",
});

export default apiClient;