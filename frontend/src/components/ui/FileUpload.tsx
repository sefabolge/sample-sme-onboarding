import { useState } from "react";
import api from "../../api/axios";

interface FileUploadProps {
  docId: number;
  onSuccess?: () => void;
}

const FileUpload = ({ docId, onSuccess }: FileUploadProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      await api.patch(`/documents/${docId}/reupload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("✅ Document re-uploaded successfully.");
      if (onSuccess) onSuccess(); // 👈 trigger refresh in parent
    } catch {
      setMessage("❌ Failed to re-upload document.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={e => setFile(e.target.files?.[0] || null)}
        disabled={uploading}
      />
      <button onClick={handleUpload} disabled={!file || uploading}>
        {uploading ? "Uploading..." : "Re-upload"}
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload;
