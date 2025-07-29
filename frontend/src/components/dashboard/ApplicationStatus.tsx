import { useEffect, useState } from "react";
import api from "../../api/axios";
import FileUpload from "../../components/ui/FileUpload";
import StatusBadge from "../../components/ui/StatusBadge";
import "../../styles/dashboard.css";

interface PushedBackDocument {
  id: number;
  status: string;
  uploaded_at: string;
  pushback_reason: string | null;
  doc_type: string;
}

interface Application {
  status: string;
  reason: string | null;
  pushed_back_document: PushedBackDocument | null;
}

const ApplicationStatus = () => {
  const [app, setApp] = useState<Application | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchApplication = async () => {
    setLoading(true);
    try {
      const response = await api.get("/application/status/");
      setApp(response.data);
    } catch (err) {
      console.error("Failed to fetch application.", err);
      setError("Failed to fetch your application. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplication();
  }, []);

  if (loading) return <p>Loading your application...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!app) return <p>No application found. Please contact support.</p>;

  const pushedBackDoc = app.pushed_back_document;

    return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Application Status</h2>

      <p>
        <strong>Status:</strong> <StatusBadge status={app.status} />
      </p>

      {app.reason && (
        <p style={{ marginTop: "1rem" }}>
          <strong>Admin Reason:</strong> {app.reason}
        </p>
      )}

      {app.status === "PUSHBACK" && pushedBackDoc && (
        <div className="section">
          <h4>🔁 Re-upload Required</h4>
          <p>
            <strong>Document Type:</strong> {pushedBackDoc.doc_type}
          </p>
          <p>
            <strong>Pushback reason:</strong> {pushedBackDoc.pushback_reason}
          </p>
          <p>
            <strong>Last upload:</strong>{" "}
            {new Date(pushedBackDoc.uploaded_at).toLocaleString()}
          </p>

          <FileUpload docId={pushedBackDoc.id} onSuccess={fetchApplication} />
        </div>
      )}

      {!pushedBackDoc && app.status === "PENDING" && (
        <div className="section">
          <p>⌛ Your application is under review. We’ll get back to you shortly.</p>
        </div>
      )}

      {app.status === "APPROVED" && (
        <div className="section">
          <p>✅ Your application has been approved. Welcome onboard!</p>
        </div>
      )}

      {app.status === "REJECTED" && (
        <div className="section">
          <p>❌ Your application has been rejected. You may contact support for more info.</p>
        </div>
      )}
    </div>
  );
};

export default ApplicationStatus;
