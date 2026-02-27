'use client';

import { ChatMessage as ChatMessageType } from '@/types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ChatMessageProps {
    message: ChatMessageType;
}

interface MetadataItem {
    shop_name: string;
    page: number;
    image_url: string;
    thumbnail_url?: string;
    product_name?: string;
    price?: string;
}

function ProductCard({ product, index, metadata }: { product: any, index: number, metadata?: MetadataItem[] }) {
    // Attempt to find a specific image for this product in the metadata
    const findMatchingImage = () => {
        if (!metadata || metadata.length === 0) return null;

        const productName = (product.Product || product.product || product.name || '').toLowerCase();
        const storeName = (product.Store || product.store || '').toLowerCase();

        // 1. Try exact or near-exact match on product_name if available in metadata
        const directMatch = metadata.find(m => {
            if (!m.product_name) return false;
            const mProd = m.product_name.toLowerCase();
            const mStore = m.shop_name.toLowerCase();
            return (mStore === storeName || storeName.includes(mStore)) &&
                (mProd === productName || mProd.includes(productName) || productName.includes(mProd));
        });

        if (directMatch) return directMatch.thumbnail_url || directMatch.image_url;

        // 2. Fallback: Just match by store name if there's only one image for that store
        // (This helps with legacy page-level results)
        const storeMatch = metadata.filter(m => m.shop_name.toLowerCase() === storeName);
        if (storeMatch.length === 1) return storeMatch[0].thumbnail_url || storeMatch[0].image_url;

        return null;
    };

    const imageUrl = findMatchingImage();

    return (
        <div key={index} className="product-card-premium animate-fade-in group" style={{ animationDelay: `${index * 100}ms` }}>
            <div className="flex justify-between items-start mb-2">
                <span className="store-tag">{product.Store || product.store || 'Store'}</span>
                <span className="badge-price text-lg leading-none">{product.Price || product.price}</span>
            </div>

            <div className="flex gap-3 mb-3">
                {imageUrl && (
                    <div className="flex-shrink-0">
                        <img
                            src={imageUrl}
                            alt={product.Product || 'Product'}
                            className="w-16 h-16 object-cover rounded-lg border border-slate-100 dark:border-slate-800 shadow-sm"
                        />
                    </div>
                )}
                <h3 className="text-sm font-semibold text-slate-800 dark:text-gray-100 flex-1 leading-relaxed line-clamp-3">
                    {product.Product || product.product || product.name || 'Product'}
                </h3>
            </div>

            {(product.Deal || product.deal) && (
                <div className="mt-auto">
                    <span className="badge-deal w-full text-center py-1">{product.Deal || product.deal}</span>
                </div>
            )}
        </div>
    );
}

export default function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === 'user';

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fade-in`}>
            <div
                className={`max-w-[92%] rounded-2xl px-4 py-3 ${isUser
                    ? 'bg-blue-600 text-white rounded-br-sm shadow-md'
                    : 'glass text-gray-900 dark:text-white rounded-bl-sm shadow-sm'
                    }`}
            >
                {isUser ? (
                    <p className="text-sm md:text-base">{message.content}</p>
                ) : (
                    <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none">
                        <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                                p: ({ children }) => <p className="mb-2 last:mb-0 text-gray-800 dark:text-gray-200">{children}</p>,
                                table: ({ children }) => {
                                    try {
                                        const head = (children as any[])?.find(c => c.type === 'thead');
                                        const body = (children as any[])?.find(c => c.type === 'tbody');

                                        if (head && body) {
                                            const headers = (head.props.children.props.children as any[]).map(th =>
                                                String(th.props.children).trim()
                                            );

                                            const isProductList = headers.some(h =>
                                                /product|name|price|store|item/i.test(h)
                                            );

                                            if (isProductList) {
                                                const rows = Array.isArray(body.props.children)
                                                    ? body.props.children
                                                    : [body.props.children];

                                                const products = rows.filter(Boolean).map((tr: any) => {
                                                    const cells = Array.isArray(tr.props.children) ? tr.props.children : [tr.props.children];
                                                    const product: any = {};
                                                    headers.forEach((header, i) => {
                                                        if (cells[i]) {
                                                            product[header] = cells[i].props.children;
                                                        }
                                                    });
                                                    return product;
                                                });

                                                return (
                                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 my-4">
                                                        {products.map((p: any, i: number) => (
                                                            <ProductCard key={i} product={p} index={i} metadata={message.metadata as MetadataItem[]} />
                                                        ))}
                                                    </div>
                                                );
                                            }
                                        }
                                    } catch (e) {
                                        console.error('Failed to parse product table:', e);
                                    }

                                    return (
                                        <div className="overflow-x-auto my-4 -mx-2 px-2 scrollbar-hide">
                                            <div className="table-premium shadow-lg">
                                                <table className="min-w-full border-separate border-spacing-0">{children}</table>
                                            </div>
                                        </div>
                                    );
                                },
                                tr: ({ children }) => (
                                    <tr className="group transition-colors">{children}</tr>
                                ),
                                thead: ({ children }) => (
                                    <thead className="bg-slate-50 dark:bg-slate-900 border-b-2 border-slate-200 dark:border-slate-800">{children}</thead>
                                ),
                                th: ({ children }) => (
                                    <th className="px-4 py-3 text-left text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap">
                                        {children}
                                    </th>
                                ),
                                td: ({ children }) => {
                                    const content = String(children).trim();
                                    const isDeal = content.includes('SAVE') ||
                                        content.includes('WAS') ||
                                        content.includes('% OFF') ||
                                        content.toLowerCase().includes('per') ||
                                        content.toLowerCase().includes('each');

                                    const isPrice = /^\$?\d+(\.\d{2})?$/.test(content) ||
                                        (content.startsWith('$') && !isNaN(parseFloat(content.substring(1))) && content.length < 10);

                                    return (
                                        <td className="px-4 py-3 border-t border-slate-100 dark:border-slate-800/50 text-sm text-slate-700 dark:text-slate-300 transition-colors group-hover:bg-blue-50/30 dark:group-hover:bg-blue-900/10">
                                            {isDeal ? (
                                                <div className="flex flex-col gap-1">
                                                    <span className="badge-deal w-fit">{children}</span>
                                                </div>
                                            ) : isPrice ? (
                                                <span className="badge-price">{children}</span>
                                            ) : (
                                                <span className="font-medium text-slate-900 dark:text-slate-100">{children}</span>
                                            )}
                                        </td>
                                    );
                                },
                            }}
                        >
                            {message.content}
                        </ReactMarkdown>
                    </div>
                )}

                {!isUser && message.metadata && message.metadata.length > 0 && (
                    <div className="mt-3 flex gap-3 overflow-x-auto pb-2 -mx-1 px-1 scrollbar-hide">
                        {message.metadata.map((item, i) => (
                            <a
                                key={i}
                                href={item.image_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex-shrink-0 relative group outline-none"
                            >
                                <div className="absolute top-1 left-1 z-10">
                                    <span className="text-[9px] font-bold bg-white/90 dark:bg-gray-800/90 px-1.5 py-0.5 rounded shadow-sm text-blue-600 uppercase tracking-tighter">
                                        {item.shop_name}
                                    </span>
                                </div>
                                <img
                                    src={item.thumbnail_url || item.image_url}
                                    alt={`Catalog page ${item.page}`}
                                    className="w-20 h-28 md:w-24 md:h-32 object-cover rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm transition-all duration-300 group-hover:shadow-md group-hover:brightness-95"
                                />
                                <div className="absolute bottom-1 right-1">
                                    <div className="bg-black/50 backdrop-blur-sm p-1 rounded-md opacity-0 group-hover:opacity-100 transition-opacity">
                                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M15 3h6v6" /><path d="M10 14 21 3" /><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" /></svg>
                                    </div>
                                </div>
                            </a>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
