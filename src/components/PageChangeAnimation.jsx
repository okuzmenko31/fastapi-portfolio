import React from 'react';
import { motion } from "framer-motion"


const animations = {
    initial: {opacity: 0, x: -100},
    animate: {opacity: 1, x: 0},
    exit: {opacity: 0, x: -100},
}
const PageChangeAnimation = ({children}) => {
    return (
        <motion.div style={{width:"100%", height:"100%", display:"flex"}} variants={animations} initial="initial" animate="animate" exit="exit">
            {children}
        </motion.div>
    );
};

export default PageChangeAnimation;