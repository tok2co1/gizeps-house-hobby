"use client";
import React from 'react';
import Header from '../../../components/Header';
import { motion } from 'framer-motion';
import { ShoppingCart, ArrowLeft, ShieldCheck, Truck, RefreshCcw } from 'lucide-react';
import Link from 'next/link';

const BASE_URL = "http://localhost:8000";

export default function ProductDetail({ params }) {
    const { id } = React.use(params);
    const [product, setProduct] = React.useState(null);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        async function fetchProduct() {
            try {
                const response = await fetch(`${BASE_URL}/product/${id}`);
                const data = await response.json();

                if (data.error) throw new Error(data.error);

                // Map relative image paths to full URLs
                const processedProduct = {
                    ...data,
                    image: data.image.startsWith('http') ? data.image : `${BASE_URL}${data.image}`
                };

                setProduct(processedProduct);
            } catch (error) {
                console.error("Error fetching product:", error);
            } finally {
                setLoading(false);
            }
        }
        fetchProduct();
    }, [id]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-white">
                <div className="w-12 h-12 border-4 border-purple border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    if (!product) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-white">
                <h2 className="text-2xl font-bold mb-4">Ürün Bulunamadı</h2>
                <Link href="/" className="text-purple hover:underline flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Mağazaya Dön
                </Link>
            </div>
        );
    }

    return (
        <main className="min-h-screen bg-white">
            <Header />

            <div className="container mx-auto px-4 md:px-8 py-12">
                <Link href="/" className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-text-muted hover:text-purple mb-12 transition-colors">
                    <ArrowLeft className="w-4 h-4" /> Geri Dön
                </Link>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
                    {/* Left: Image */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="bg-gray-50 rounded-3xl overflow-hidden aspect-square flex items-center justify-center p-8 sticky top-32"
                    >
                        <img
                            src={product.image}
                            alt={product.title}
                            className="w-full h-full object-contain mix-blend-multiply transition-transform duration-700 hover:scale-110"
                        />
                    </motion.div>

                    {/* Right: Info */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="flex flex-col"
                    >
                        <span
                            className="text-xs font-bold text-purple uppercase tracking-[0.3em] mb-4"
                            style={{ fontFamily: 'var(--font-pacifico)' }}
                        >
                            {product.category}
                        </span>
                        <h1
                            className="text-4xl md:text-6xl font-bold text-text-main leading-tight mb-6"
                            style={{ fontFamily: 'var(--font-pacifico)' }}
                        >
                            {product.title}
                        </h1>
                        <p className="text-2xl font-bold text-black mb-8">
                            {product.price} ₺
                        </p>

                        <div className="prose prose-sm text-text-muted mb-10 leading-relaxed">
                            <p>{product.description || "Bu ürün özel tasarım rub-on transfer tekniği ile hazırlanmıştır. Her türlü sert yüzeye kolayca uygulanabilir."}</p>
                        </div>

                        <div className="flex flex-col gap-4 mb-12">
                            <button className="w-full bg-black text-white py-5 px-8 font-black uppercase tracking-widest text-xs hover:bg-purple hover:text-black transition-all duration-300 flex items-center justify-center gap-3">
                                <ShoppingCart className="w-4 h-4" /> SEPETE EKLE
                            </button>
                            <p className="text-[10px] text-text-muted text-center uppercase tracking-widest">
                                STOK KODU: {product.sku}
                            </p>
                        </div>

                        {/* Features */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8 border-t border-gray-100">
                            <div className="flex flex-col items-center text-center">
                                <Truck className="w-5 h-5 text-zinc-400 mb-3" />
                                <span className="text-[10px] font-bold uppercase tracking-widest">HIZLI KARGO</span>
                            </div>
                            <div className="flex flex-col items-center text-center">
                                <ShieldCheck className="w-5 h-5 text-zinc-400 mb-3" />
                                <span className="text-[10px] font-bold uppercase tracking-widest">GÜVENLİ ÖDEME</span>
                            </div>
                            <div className="flex flex-col items-center text-center">
                                <RefreshCcw className="w-5 h-5 text-zinc-400 mb-3" />
                                <span className="text-[10px] font-bold uppercase tracking-widest">KOLAY İADE</span>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Application Guide */}
            <section className="bg-gray-50 py-24 mt-24">
                <div className="container mx-auto px-4 md:px-8">
                    <div className="max-w-3xl mx-auto text-center">
                        <h2 className="text-3xl font-serif font-bold italic mb-12">Nasıl Uygulanır?</h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            {[
                                { step: "01", t: "TEMİZLE", d: "Yüzeyi kirden ve tozdan arındırın." },
                                { step: "02", t: "UYGULA", d: "Transferi yüzeye yerleştirin ve baskı uygulayın." },
                                { step: "03", t: "SOYUN", d: "Üstteki koruyucu film tabakasını yavaşça çıkarın." }
                            ].map((s, i) => (
                                <div key={i} className="flex flex-col">
                                    <span className="text-5xl font-serif font-bold text-gray-200 mb-4">{s.step}</span>
                                    <h4 className="font-black text-xs tracking-widest mb-2 uppercase">{s.t}</h4>
                                    <p className="text-xs text-text-muted uppercase leading-tight font-medium">{s.d}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>
        </main>
    );
}
