import { useEffect, useRef, useState } from "react";
import Dashboard from "./pages/Dashboard";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import { useAuth } from "./hooks/useAuth";

function App() {
  const [isNavVisible, setIsNavVisible] = useState(true);
  const [path, setPath] = useState(window.location.pathname);
  const lastScrollY = useRef(0);
  const { isAuthenticated, loading } = useAuth();

  const navigate = (to: string) => {
    if (window.location.pathname === to) return;
    window.history.pushState({}, "", to);
    setPath(to);
    window.scrollTo({ top: 0, behavior: "auto" });
  };

  useEffect(() => {
    const onPopState = () => setPath(window.location.pathname);
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  useEffect(() => {
    if (path !== "/") return;
    const onScroll = () => {
      const currentY = window.scrollY;

      if (currentY < 24) {
        setIsNavVisible(true);
      } else if (currentY > lastScrollY.current + 8) {
        setIsNavVisible(false);
      } else if (currentY < lastScrollY.current - 8) {
        setIsNavVisible(true);
      }

      lastScrollY.current = currentY;
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [path]);

  useEffect(() => {
    if (path === "/signup") navigate("/login");
  }, [path]);

  useEffect(() => {
    if (path === "/dashboard" && !loading && !isAuthenticated) {
      navigate("/login");
    }
  }, [path, loading, isAuthenticated]);

  useEffect(() => {
    if (path === "/login" && !loading && isAuthenticated) {
      navigate("/dashboard");
    }
  }, [path, loading, isAuthenticated]);

  return (
    <div className="min-h-screen bg-black text-slate-100">
      <header
        className={`fixed left-0 top-0 z-30 w-full transition-all duration-500 ease-out ${
          path !== "/" || isNavVisible ? "translate-y-0 opacity-100" : "-translate-y-full opacity-0"
        }`}
      >
        <div className="flex w-full items-center justify-between border-b border-white/10 bg-slate-950/45 px-5 py-3 text-[11px] uppercase tracking-[0.12em] text-slate-200 backdrop-blur-md md:px-8 md:py-3.5">
          <a
            href="/"
            onClick={(e) => {
              e.preventDefault();
              navigate("/");
            }}
            className="text-xl font-extrabold tracking-tight text-slate-100"
          >
            Sentinel
          </a>
          <nav className="flex items-center gap-8">
            <a
              href="/#features"
              onClick={(e) => {
                if (path !== "/") return;
                e.preventDefault();
                document.getElementById("features")?.scrollIntoView({ behavior: "smooth" });
              }}
              className="transition hover:text-white"
            >
              Core Features
            </a>
            <a
              href="/login"
              onClick={(e) => {
                e.preventDefault();
                navigate("/login");
              }}
              className="transition hover:text-white"
            >
              Login
            </a>
            <a
              href="/dashboard"
              onClick={(e) => {
                e.preventDefault();
                if (!isAuthenticated) {
                  navigate("/login");
                  return;
                }
                navigate("/dashboard");
              }}
              className="transition hover:text-white"
            >
              Dashboard
            </a>
          </nav>
        </div>
      </header>

      <main>
        {path === "/" ? <Landing /> : null}
        {path === "/login" ? <Login onSuccess={() => navigate("/dashboard")} /> : null}
        {path === "/dashboard" ? (
          loading ? (
            <div className="flex min-h-screen items-center justify-center bg-black text-slate-300">
              Checking session...
            </div>
          ) : isAuthenticated ? (
            <Dashboard onLogout={() => navigate("/login")} />
          ) : null
        ) : null}
      </main>
    </div>
  );
}

export default App;
