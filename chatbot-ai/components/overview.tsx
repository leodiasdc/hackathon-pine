import { motion } from 'framer-motion';
import Link from 'next/link';
import Image from 'next/image';
import { MessageIcon, VercelIcon } from './icons';

export const Overview = () => {
  return (
    <motion.div
      key="overview"
      className="max-w-3xl mx-auto md:mt-20"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ delay: 0.5 }}
    >
      <div className="rounded-xl p-6 flex flex-col gap-8 leading-relaxed text-center max-w-xl">
        <p className="flex flex-row justify-center gap-4 items-center">
          <Image
            src="/images/banco_pine.jpg"
            alt="Logo do BancoPine" 
            width={100}
            height={100}
            className="squared-full"
          />
        </p>
        <p>
        Bem-vindo ao ChatBot do Banco Pine, o PineBot! Aqui, estamos prontos para atender suas necessidades de forma rápida, fácil e personalizada.
        </p>
        <p> 
          Você pode visitar o nosso&nbsp;
          <Link
            className="font-medium underline underline-offset-4"
            href="https://www.pine.com"
            target="_blank"
          >
          site
          </Link>
          &nbsp;aqui.
        </p>
      </div>
    </motion.div>
  );
};
