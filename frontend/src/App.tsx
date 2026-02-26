import { useEffect, useRef, useState } from "react";

import Analyses from "./pages/Analyses";
import Analysis from "./pages/Analysis";
import Contact from "./pages/Contact";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Privacy from "./pages/Privacy";
import Report from "./pages/Report";
import Upload from "./pages/Upload";
import { useAuth } from "./hooks/useAuth";
import { supabase } from "./lib/supabase";

function App() {
  const [isNavVisible, setIsNavVisible] = useState(true);
  const [path, setPath] = useState(window.location.pathname);
  const [pendingUploadFile, setPendingUploadFile] = useState<File | null>(null);
  const lastScrollY = useRef(0);
  const { isAuthenticated, loading } = useAuth();

  const analysisMatch = path.match(/^\/analysis\/([^/]+)$/);
  const reportMatch = path.match(/^\/report\/([^/]+)$/);
  const analysisDatasetId = analysisMatch ? decodeURIComponent(analysisMatch[1]) : null;
  const reportDatasetId = reportMatch ? decodeURIComponent(reportMatch[1]) : null;

  const navigate = (to: string) => {
    if (window.location.pathname === to) return;
    window.history.pushState({}, "", to);
    setPath(to);
    window.scrollTo({ top: 0, behavior: "auto" });
  };

  const logout = async () => {
    if (supabase) {
      await supabase.auth.signOut();
    }
    navigate("/login");
  };

  useEffect(() => {
    const onPopState = () => setPath(window.location.pathname);
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  useEffect(() => {
    lastScrollY.current = window.scrollY;
    setIsNavVisible(true);

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
    const protectedPaths = ["/analyses", "/dashboard"];
    if (protectedPaths.includes(path) && !loading && !isAuthenticated) {
      navigate("/login");
    }
  }, [path, loading, isAuthenticated]);

  useEffect(() => {
    if (path === "/login" && !loading && isAuthenticated) {
      navigate("/analyses");
    }
  }, [path, loading, isAuthenticated]);

  return (
    <div className="min-h-screen bg-black text-slate-100">
      <header
        className={`fixed left-0 top-0 z-30 w-full transition-all duration-500 ease-out ${
          isNavVisible ? "translate-y-0 opacity-100" : "-translate-y-full opacity-0"
        }`}
      >
        <div className="flex w-full items-center justify-between border-b border-white/10 bg-slate-950/45 px-5 py-3 text-[11px] uppercase tracking-[0.12em] text-slate-200 backdrop-blur-md md:px-8 md:py-3.5">
          <a
            href="/"
            onClick={(e) => {
              e.preventDefault();
              navigate("/");
            }}
            className="instrument-serif-regular text-2xl tracking-tight text-slate-100"
          >
            Sentinel
          </a>

          <nav className="flex items-center gap-8">
            {isAuthenticated ? (
              <button type="button" onClick={logout} className="transition hover:text-white">
                LOGOUT
              </button>
            ) : (
              <a
                href="/login"
                onClick={(e) => {
                  e.preventDefault();
                  navigate("/login");
                }}
                className="transition hover:text-white"
              >
                LOGIN
              </a>
            )}

            <a
              href="/analyses"
              onClick={(e) => {
                e.preventDefault();
                if (!isAuthenticated) {
                  navigate("/login");
                  return;
                }
                navigate("/analyses");
              }}
              className="normal-case transition hover:text-white"
            >
              ANALYSES
            </a>
          </nav>
        </div>
      </header>

      <main>
        {path === "/" ? (
          <Landing
            onUploadFile={(file) => {
              setPendingUploadFile(file);
              navigate("/upload");
            }}
            onNavigateUpload={() => navigate("/upload")}
            onNavigatePrivacy={() => navigate("/privacy")}
            onNavigateContact={() => navigate("/contact")}
          />
        ) : null}

        {path === "/upload" ? (
          <Upload
            initialFile={pendingUploadFile}
            onUploaded={(datasetId) => {
              setPendingUploadFile(null);
              navigate(`/report/${datasetId}`);
            }}
          />
        ) : null}

        {path === "/login" ? <Login onSuccess={() => navigate("/analyses")} /> : null}
        {path === "/privacy" ? <Privacy /> : null}
        {path === "/contact" ? <Contact /> : null}

        {path === "/analyses" ? (
          loading ? (
            <div className="flex min-h-screen items-center justify-center bg-black text-slate-300">
              Checking session...
            </div>
          ) : isAuthenticated ? (
            <Analyses
              onOpenAnalysis={(datasetId) => navigate(`/analysis/${datasetId}`)}
              onViewReport={(datasetId) => navigate(`/report/${datasetId}`)}
            />
          ) : null
        ) : null}

        {analysisDatasetId ? (
          <Analysis
            datasetId={analysisDatasetId}
            onGoAnalyses={() => navigate("/analyses")}
            onViewReport={(datasetId) => navigate(`/report/${datasetId}`)}
          />
        ) : null}

        {reportDatasetId ? (
          <Report
            datasetId={reportDatasetId}
            onBackToDashboard={() => navigate(isAuthenticated ? "/analyses" : "/upload")}
            onDeleted={() => navigate(isAuthenticated ? "/analyses" : "/upload")}
          />
        ) : null}
      </main>
    </div>
  );
}

export default App;
