const colors: Record<string, string> = {
  PENDING: "gray",
  APPROVED: "green",
  REJECTED: "red",
  PUSHBACK: "orange",
};

const StatusBadge = ({ status }: { status: string }) => {
  const color = colors[status.toUpperCase()] || "black";
  return (
    <span style={{ color, fontWeight: "bold", textTransform: "capitalize" }}>
      {status}
    </span>
  );
};

export default StatusBadge;
