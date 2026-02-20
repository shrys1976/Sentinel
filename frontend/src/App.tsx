import { useEffect, useRef, useState } from "react";
import Landing from "./pages/Landing";

function App() {
  const [isNavVisible, setIsNavVisible] = useState(true);
  const lastScrollY = useRef(0);

  useEffect(() => {
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
  }, []);

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header
        className={`fixed left-0 top-0 z-30 w-full transition-all duration-500 ease-out ${
          isNavVisible ? "translate-y-0 opacity-100" : "-translate-y-full opacity-0"
        }`}
      >
        <div className="mx-auto flex w-[min(1240px,calc(100vw-36px))] items-center justify-between border-b border-white/10 bg-slate-950/45 px-4 py-4 text-[11px] uppercase tracking-[0.12em] text-slate-200 backdrop-blur-md md:py-5">
          <a href="#top" className="text-xl font-extrabold lowercase tracking-tight text-slate-100">
            sentinelai
          </a>
          <nav className="flex items-center gap-8">
            <a href="#features" className="transition hover:text-white">
              Core Features
            </a>
            <a href="#signup" className="transition hover:text-white">
              Signup
            </a>
            <a href="#dashboard" className="transition hover:text-white">
              Dashboard
            </a>
          </nav>
        </div>
      </header>

      <main>
        <Landing />
      </main>
    </div>
  );
}

export default App;
