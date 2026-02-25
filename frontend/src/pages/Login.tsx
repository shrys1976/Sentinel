import { FormEvent, useMemo, useState } from "react";
import { isSupabaseConfigured, supabase } from "../lib/supabase";

type LoginProps = {
  onSuccess: () => void;
};

export default function Login({ onSuccess }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  const emailRedirectTo = useMemo(
    () => `${window.location.origin}/login`,
    []
  );

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setInfo(null);

    if (!isSupabaseConfigured || !supabase) {
      setError("Auth is not configured. Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
      return;
    }

    if (!email.trim() || !password.trim()) {
      setError("Email and password are required.");
      return;
    }

    setSubmitting(true);
    try {
      const signIn = await supabase.auth.signInWithPassword({
        email: email.trim(),
        password,
      });

      if (!signIn.error && signIn.data.session) {
        onSuccess();
        return;
      }

      const signInError = signIn.error?.message ?? "Unable to login.";
      if (signInError.toLowerCase().includes("email not confirmed")) {
        setError("Email is not verified. Please confirm your inbox first.");
        return;
      }

      const signUp = await supabase.auth.signUp({
        email: email.trim(),
        password,
        options: { emailRedirectTo },
      });

      if (signUp.error) {
        const msg = signUp.error.message.toLowerCase();
        if (msg.includes("already") || msg.includes("registered")) {
          setError("Incorrect email or password.");
          return;
        }
        setError(signUp.error.message);
        return;
      }

      setInfo("Account created. Check your email to confirm, then login.");
      setTimeout(() => {
        window.location.href = "/login";
      }, 1200);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-black px-5 py-24 text-slate-100">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-slate-950/70 p-7 backdrop-blur-sm">
        <h1 className="instrument-serif-regular text-4xl tracking-tight">Login</h1>
        {!isSupabaseConfigured ? (
          <p className="mt-3 rounded-lg border border-amber-400/30 bg-amber-500/10 px-3 py-2 text-xs text-amber-200">
            Missing Supabase env vars. Add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.
          </p>
        ) : null}

        <form onSubmit={submit} className="mt-6 space-y-4">
          <label className="block text-sm">
            <span className="mb-1 block text-slate-300">Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-xl border border-white/15 bg-black/60 px-3 py-2 text-slate-100 outline-none transition focus:border-white/40"
              placeholder="you@example.com"
              autoComplete="email"
            />
          </label>

          <label className="block text-sm">
            <span className="mb-1 block text-slate-300">Password</span>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-xl border border-white/15 bg-black/60 px-3 py-2 pr-10 text-slate-100 outline-none transition focus:border-white/40"
                placeholder="••••••••"
                autoComplete="current-password"
              />
              <button
                type="button"
                onClick={() => setShowPassword((prev) => !prev)}
                className="absolute inset-y-0 right-0 flex items-center px-3 text-slate-400 transition hover:text-slate-200"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? "🙈" : "👁"}
              </button>
            </div>
          </label>

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}
          {info ? <p className="text-sm text-emerald-300">{info}</p> : null}

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? "Processing..." : "Continue"}
          </button>
        </form>
      </div>
    </div>
  );
}
