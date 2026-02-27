'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { Menu, User, Star, LogOut } from 'lucide-react';
import { Menu as HeadlessMenu } from '@headlessui/react';
import Link from 'next/link';

export default function Header() {
    const { user, logout } = useAuth();
    const router = useRouter();

    const handleLogout = async () => {
        await logout();
        router.push('/login');
    };

    return (
        <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3">
            <div className="max-w-7xl mx-auto flex items-center justify-between">
                <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                        <h1 className="text-xl font-extrabold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
                            <span className="bg-blue-600 text-white p-1 rounded-lg shadow-sm">NA</span>
                            Niyogen Assistant
                        </h1>
                        <span className="badge-australia">AU</span>
                    </div>
                    <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium ml-10 -mt-1 uppercase tracking-widest">Smart Price Comparison</p>
                </div>

                <HeadlessMenu as="div" className="relative">
                    <HeadlessMenu.Button className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                            <User className="w-5 h-5 text-white" />
                        </div>
                        <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                    </HeadlessMenu.Button>

                    <HeadlessMenu.Items className="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 focus:outline-none z-50">
                        <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
                            <p className="text-sm font-medium text-gray-900 dark:text-white">
                                {user?.name}
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                                {user?.email}
                            </p>
                        </div>

                        <HeadlessMenu.Item>
                            {({ active }) => (
                                <Link
                                    href="/reviews"
                                    className={`flex items-center gap-3 px-4 py-2 text-sm ${active
                                        ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                                        : 'text-gray-700 dark:text-gray-300'
                                        }`}
                                >
                                    <Star className="w-4 h-4" />
                                    Reviews & Ratings
                                </Link>
                            )}
                        </HeadlessMenu.Item>

                        <HeadlessMenu.Item>
                            {({ active }) => (
                                <button
                                    onClick={handleLogout}
                                    className={`w-full flex items-center gap-3 px-4 py-2 text-sm ${active
                                        ? 'bg-gray-100 dark:bg-gray-700 text-red-600 dark:text-red-400'
                                        : 'text-red-600 dark:text-red-400'
                                        }`}
                                >
                                    <LogOut className="w-4 h-4" />
                                    Logout
                                </button>
                            )}
                        </HeadlessMenu.Item>
                    </HeadlessMenu.Items>
                </HeadlessMenu>
            </div>
        </header>
    );
}
