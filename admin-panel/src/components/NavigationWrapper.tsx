'use client';

import { usePathname } from "next/navigation";
import Sidebar from "./Sidebar";
import Header from "./Header";

export default function NavigationWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isLoginPage = pathname === '/login';

  return (
    <div className="flex bg-dashboard-grid transition-all duration-300">
      {/* Sidebar - Fixed */}
      {!isLoginPage && <Sidebar />}

      {/* Main Content Area */}
      <div className={`flex-1 flex flex-col ${isLoginPage ? 'ml-0' : 'ml-64'} min-h-screen transition-all duration-300`}>
        {/* Header - Sticky */}
        {!isLoginPage && <Header />}

        {/* Page Content */}
        <main className="flex-1 px-8 py-8 transition-all duration-300">
          <div className="max-w-7xl mx-auto h-full">
            {children}
          </div>
        </main>

        {/* Footer Placeholder (Optional) */}
        <footer className="px-8 py-6 text-center text-gray-600 text-[10px] font-medium tracking-widest uppercase">
          © 2026 AdminHub Suite • All systems operational
        </footer>
      </div>
    </div>
  );
}
