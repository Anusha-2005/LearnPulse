"use client";

import { ArrowRight, Mail, Lock, Loader2, AlertCircle, ChevronLeft } from "lucide-react";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/useAuthStore";
import { authService } from "@/services/auth";

export default function LoginPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const [isForgotMode, setIsForgotMode] = useState(false);
    const [success, setSuccess] = useState("");
    const [formData, setFormData] = useState({
        email: "",
        password: ""
    });

    const login = useAuthStore((state) => state.login);

    const handleForgotPassword = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError("");
        setSuccess("");

        try {
            await authService.forgotPassword(formData.email);
            setSuccess("If an account exists, a reset link has been sent.");
            setTimeout(() => {
                setIsForgotMode(false);
                setSuccess("");
            }, 3000);
        } catch (err: any) {
            setError("Failed to process reset request.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError("");
        setSuccess("");

        try {
            const data = await authService.login(formData.email, formData.password);

            const user = {
                id: data.user_id,
                email: formData.email,
                name: data.name || formData.email.split("@")[0].replace(/[._]/g, " ").replace(/\b\w/g, c => c.toUpperCase()),
                role: data.role,
                student_id: data.student_id
            };

            login(user, data.access_token);
            router.push("/dashboard");
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || "Login failed. Check your credentials.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="bg-white/90 dark:bg-neutral-900/90 backdrop-blur-xl p-10 rounded-3xl shadow-2xl border border-white/40 dark:border-neutral-800/50 max-w-md w-full transition-all duration-300 ring-1 ring-black/5 dark:ring-white/5 relative overflow-hidden">
            {/* Top decorative gradient line */}
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500"></div>

            <div className="text-center mb-8">
                <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight">Welcome to LearnPulse</h2>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium">Sign in to monitor student risk and performance.</p>
            </div>

            {error && (
                <div className="mb-6 bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 p-3.5 rounded-xl text-sm flex items-center gap-2 border border-red-100 dark:border-red-900/30 animate-in slide-in-from-top-2">
                    <AlertCircle size={16} />
                    {error}
                </div>
            )}

            {success && (
                <div className="mb-6 bg-green-50 dark:bg-green-950/30 text-green-600 dark:text-green-400 p-3.5 rounded-xl text-sm flex items-center gap-2 border border-green-100 dark:border-green-900/30 animate-in slide-in-from-top-2">
                    <Loader2 size={16} className="animate-spin" />
                    {success}
                </div>
            )}

            {isForgotMode ? (
                <form onSubmit={handleForgotPassword} className="space-y-4 animate-in slide-in-from-right-8 duration-300">
                    <div>
                        <label className="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-2 ml-1">Email Address</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500" size={18} />
                            <input
                                type="email"
                                required
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                className="w-full pl-10 pr-4 py-3 bg-neutral-50/50 dark:bg-neutral-950/40 border border-neutral-200 dark:border-neutral-800/80 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white dark:focus:bg-neutral-900 transition-all text-gray-900 dark:text-white"
                                placeholder="name@university.edu"
                            />
                        </div>
                    </div>

                    <div className="pt-2">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/35 transition-all transform hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98]"
                        >
                            {isLoading ? <Loader2 className="animate-spin" size={20} /> : "Send Reset Link"}
                        </button>
                    </div>

                    <button
                        type="button"
                        onClick={() => setIsForgotMode(false)}
                        className="w-full text-center text-sm text-gray-400 hover:text-gray-600 font-medium py-2 flex items-center justify-center gap-1 transition-colors"
                    >
                        <ChevronLeft size={14} /> Back to login
                    </button>
                </form>
            ) : (
                <form onSubmit={handleSubmit} className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-2 ml-1">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500" size={18} />
                                <input
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="w-full pl-10 pr-4 py-3 bg-neutral-50/50 dark:bg-neutral-950/40 border border-neutral-200 dark:border-neutral-800/80 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white dark:focus:bg-neutral-900 transition-all text-gray-900 dark:text-white"
                                    placeholder="name@university.edu"
                                />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between items-center mb-2 ml-1">
                                <label className="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider">Password</label>
                                <button
                                    type="button"
                                    onClick={() => setIsForgotMode(true)}
                                    className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline"
                                >
                                    Forgot password?
                                </button>
                            </div>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500" size={18} />
                                <input
                                    type="password"
                                    required
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    className="w-full pl-10 pr-4 py-3 bg-neutral-50/50 dark:bg-neutral-950/40 border border-neutral-200 dark:border-neutral-800/80 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white dark:focus:bg-neutral-900 transition-all text-gray-900 dark:text-white"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="pt-2">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex items-center justify-center gap-2 py-3.5 rounded-xl font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/35 transition-all transform hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98]"
                        >
                            {isLoading ? (
                                <Loader2 className="animate-spin" size={20} />
                            ) : (
                                <>
                                    Login <ArrowRight size={18} />
                                </>
                            )}
                        </button>
                    </div>
                </form>
            )}

            <div className="mt-8 pt-6 border-t border-gray-100 dark:border-neutral-800/60">
                <div className="rounded-xl bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100/50 dark:border-indigo-900/30 p-4 text-center">
                    <p className="text-xs text-indigo-700 dark:text-indigo-300 font-medium">
                        Demo Credentials:
                    </p>
                    <p className="text-xs font-mono text-indigo-600 dark:text-indigo-400 mt-1.5 select-all">
                        faculty1@gmail.com / password
                    </p>
                </div>
            </div>
        </div>
    );
}
