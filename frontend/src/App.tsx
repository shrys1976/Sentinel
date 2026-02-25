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
    <div className="min-h-screen bg-black text-slate-100">
      <header
        className={`fixed left-0 top-0 z-30 w-full transition-all duration-500 ease-out ${
          isNavVisible ? "translate-y-0 opacity-100" : "-translate-y-full opacity-0"
        }`}
      >
        <div className="flex w-full items-center justify-between border-b border-white/10 bg-slate-950/45 px-5 py-3 text-[11px] uppercase tracking-[0.12em] text-slate-200 backdrop-blur-md md:px-8 md:py-3.5">
          <a href="#top" className="text-xl font-extrabold tracking-tight text-slate-100">
            Sentinel
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
