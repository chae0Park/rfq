import "./globals.css";

export const metadata = {
  title: "RFQ Dashboard",
  description: "AI Ops Dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}