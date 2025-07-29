import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../../api/axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../utils/constant";
import "../../styles/auth/AuthForm.css"

const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await api.post("/token/", formData);
      localStorage.setItem(ACCESS_TOKEN, response.data.access);
      localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed.");
    }
  };

  return (
  <div className="auth-container">
    <form onSubmit={handleSubmit} className="auth-form">
      <h2>Login</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      <input
        type="text"
        name="username"
        placeholder="Username"
        value={formData.username}
        onChange={handleChange}
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
        required
      />
      <button type="submit">Login</button>

      <p>
        Don't have an account?{" "}
        <Link to="/signup" style={{ textDecoration: "underline" }}>
          Sign Up
        </Link>
      </p>
    </form>
  </div>
);
};

export default Login;
