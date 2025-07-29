
import React, { useState } from "react";
import { signup, login } from "../../api/auth";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import "../../styles/auth/AuthForm.css"

const SignUpPage = () => {
  const [formData, setFormData] = useState({
    username: "",
    full_name: "",
    password: "",
    certificate: null as File | null,
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { setAuthenticated } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = new FormData();
    data.append("username", formData.username);
    data.append("full_name", formData.full_name);
    data.append("password", formData.password);
    if (formData.certificate) {
      data.append("certificate", formData.certificate);
    }

    try {
      await signup(data);
      await login(formData.username, formData.password);
      setAuthenticated(true);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Signup failed.");
    }
  };

  return (
  <div className="auth-container">
    <form onSubmit={handleSubmit} className="auth-form">
      <h2>Sign Up</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
      <input name="username" placeholder="Username" onChange={handleChange} required />
      <input name="full_name" placeholder="Full Name" onChange={handleChange} required />
      <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
      <input name="certificate" type="file" onChange={handleChange} required />
      <button type="submit">Sign Up</button>
    </form>
  </div>
);
};

export default SignUpPage;
