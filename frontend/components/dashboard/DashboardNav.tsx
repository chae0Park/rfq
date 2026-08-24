"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import styles from "./DashboardNav.module.css";


export default function DashboardNav() {
  const pathname = usePathname();

  return (
    <nav className={styles.nav}>
      <Link
        href="/"
        className={`${styles.link} ${
          pathname === "/" ? styles.active : ""
        }`}
      >
        RFQ Dashboard
      </Link>

      <Link
        href="/monitoring"
        className={`${styles.link} ${
          pathname.startsWith("/monitoring")
            ? styles.active
            : ""
        }`}
      >
        AI Monitoring
      </Link>
    </nav>
  );
}