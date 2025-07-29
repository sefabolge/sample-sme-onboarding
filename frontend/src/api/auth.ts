import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN} from "../utils/constant";
import API_BASE_URL from "../utils/config";
const client = axios.create({
  baseURL: API_BASE_URL,
});

export const signup = async (formData: FormData) => {
  const response = await client.post("/signup/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

export const login = async (username: string, password: string) => {
  const response = await client.post("/token/", { username, password });
  localStorage.setItem(ACCESS_TOKEN, response.data.access);
  localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
  return response.data;
};

export const getApplication = async () => {
  const token = localStorage.getItem(ACCESS_TOKEN);
  const response = await client.get("/application/status/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};
