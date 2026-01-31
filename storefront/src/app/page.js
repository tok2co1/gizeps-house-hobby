"use client";
import React from 'react';
import Header from '../components/Header';
import ProductGrid from '../components/ProductGrid';
import { motion } from 'framer-motion';

const MOCK_PRODUCTS = [
  {
    id: 1,
    title: "Mavi Kristal Çiçek Bahçesi",
    category: "RUB ON TRANSFER",
    price: "185",
    sku: "GZP-FLW-001",
    image: "/uploaded-products/blue-flowers.jpg",
    isNew: true
  },
  {
    id: 2,
    title: "Dört Mevsim Hobi Kutusu",
    category: "RUB ON TRANSFER",
    price: "210",
    sku: "GZP-BOX-002",
    image: "/uploaded-products/hobby-boxes.jpg",
    isNew: true
  },
  {
    id: 3,
    title: "Zarif Küpe Çiçeği (Fuchsia)",
    category: "RUB ON TRANSFER",
    price: "145",
    sku: "GZP-FLW-003",
    image: "/uploaded-products/fuchsia.jpg",
    isNew: false
  },
  {
    id: 4,
    title: "Tavşanlı Sebze Sepeti İllüstrasyonu",
    category: "RUB ON TRANSFER",
    price: "165",
    sku: "GZP-ANI-004",
    image: "/uploaded-products/rabbit.jpg",
    isNew: false
  },
  {
    id: 5,
    title: "Bahar Dalları ve Şarkı Söyleyen Kuşlar",
    category: "RUB ON TRANSFER",
    price: "195",
    sku: "GZP-ANI-005",
    image: "/uploaded-products/birds.jpg",
    isNew: true
  }
];

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [products, setProducts] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [selectedCategory, setSelectedCategory] = React.useState("TÜMÜ");

  React.useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await fetch(`${BASE_URL}/products`);
        const data = await response.json();

        // Map relative image paths to full URLs
        const processedData = data.map(p => ({
          ...p,
          image: p.image.startsWith('http') ? p.image : `${BASE_URL}${p.image}`
        }));

        setProducts(processedData);
      } catch (error) {
        console.error("Error fetching products:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchProducts();
  }, []);
  return (
    <main className="min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="relative h-[500px] md:h-[750px] w-full overflow-hidden bg-black">
        <motion.img
          initial={{ scale: 1.15, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{
            scale: { duration: 8, ease: "easeOut" },
            opacity: { duration: 1.2, ease: "easeOut" }
          }}
          src="/hero-bg.png"
          alt="Hero"
          className="w-full h-full object-cover brightness-[0.6] will-change-transform"
          style={{ willChange: 'transform' }}
        />

        <div className="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-4">
          <motion.h1
            initial="hidden"
            animate="visible"
            variants={{
              visible: {
                transition: {
                  staggerChildren: 0.08
                }
              }
            }}
            className="text-6xl md:text-9xl text-purple drop-shadow-lg tracking-normal mb-12"
            style={{ fontFamily: 'var(--font-pacifico)' }}
          >
            {"Gizep's Hobby House".split("").map((char, index) => (
              <motion.span
                key={index}
                variants={{
                  hidden: { opacity: 0, y: 5 },
                  visible: { opacity: 1, y: 0 }
                }}
              >
                {char}
              </motion.span>
            ))}
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            className="mt-10 text-2xl md:text-3xl font-pacifico text-purple/80 drop-shadow-md tracking-wider"
          >
            sihirli dokunuşlar, sonsuz tasarımlar
          </motion.p>

          <motion.div
            initial={{ opacity: 0, scale: 0.85 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1.5, type: "spring", stiffness: 100 }}
          >
            <button className="mt-12 group relative bg-white overflow-hidden py-5 px-12 transition-all duration-300">
              <span className="relative z-10 text-black font-black text-sm tracking-widest uppercase group-hover:text-white transition-colors duration-300">
                FABRİKAYA GİRİŞ YAP
              </span>
              <div className="absolute inset-0 bg-purple translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
            </button>
          </motion.div>
        </div>
      </section>

      {/* Featured Products */}
      {loading ? (
        <div className="py-24 flex justify-center items-center">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : (
        <ProductGrid
          products={products.filter(p => selectedCategory === "TÜMÜ" || p.category === selectedCategory)}
          categories={["TÜMÜ", ...new Set(products.map(p => p.category))]}
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-gray-100 py-16 bg-gray-50">
        <div className="container mx-auto px-4 md:px-8 grid grid-cols-1 md:grid-cols-4 gap-12">
          <div className="col-span-1 md:col-span-1">
            <h4 className="text-2xl font-pacifico text-purple mb-6">Gizep's Hobby House</h4>
            <p className="text-xs text-text-muted leading-relaxed">
              Özel tasarım rub-on transferler ve yaratıcı hobi çözümleri. Gizep's Hobby House ile kendi tarzınızı yaratın.
            </p>
          </div>
          <div>
            <h4 className="text-sm font-bold mb-6 tracking-widest uppercase">KURUMSAL</h4>
            <ul className="text-xs space-y-4 text-text-muted">
              <li><a href="#" className="hover:text-primary transition-colors">Hakkımızda</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">İletişim</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">KVKK Aydınlatma</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-bold mb-6 tracking-widest uppercase">YARDIM</h4>
            <ul className="text-xs space-y-4 text-text-muted">
              <li><a href="#" className="hover:text-primary transition-colors">Nasıl Uygulanır?</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Kargo ve Teslimat</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">İade Politikası</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-bold mb-6 tracking-widest uppercase">BÜLTEN</h4>
            <p className="text-[10px] text-text-muted mb-4 uppercase tracking-tighter">Yeni tasarımlardan anında haberdar olun.</p>
            <div className="flex">
              <input type="email" placeholder="E-POSTA" className="bg-white border border-gray-200 px-4 py-3 text-[10px] flex-1 focus:outline-none focus:border-primary" />
              <button className="bg-primary px-6 py-3 text-[10px] font-bold">KAYDOL</button>
            </div>
          </div>
        </div>
        <div className="container mx-auto px-4 md:px-8 mt-16 pt-8 border-t border-gray-200 text-center">
          <p className="text-[10px] text-text-muted tracking-widest uppercase">&copy; 2026 GİZEP'S HOBBY HOUSE. TÜM HAKLARI SAKLIDIR.</p>
        </div>
      </footer>
    </main>
  );
}
