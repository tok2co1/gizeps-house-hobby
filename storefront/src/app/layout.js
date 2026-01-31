import { Playfair_Display, Inter, Pacifico } from "next/font/google";
import "./globals.css";

const playfair = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const pacifico = Pacifico({
  weight: "400",
  variable: "--font-pacifico",
  subsets: ["latin"],
});

export const metadata = {
  title: "GİZEP'S HOBBY HOUSE",
  description: "Özel Tasarım Rub-on Transferler ve Hobi Çözümleri",
};

import { DealerProvider } from "../context/DealerContext";

export default function RootLayout({ children }) {
  return (
    <html lang="tr">
      <body
        className={`${playfair.variable} ${inter.variable} ${pacifico.variable} antialiased`}
      >
        <DealerProvider>
          {children}
        </DealerProvider>
      </body>
    </html>
  );
}
