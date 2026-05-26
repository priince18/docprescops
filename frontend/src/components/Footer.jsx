import React from 'react'
import { assets } from '../assets/assets'

const Footer = () => {
  return (
    <div className='bg-gray-100 rounded-lg '>
    <div className='md:mx-10 '>
        <div className='flex flex-col sm:grid grid-cols-[3fr_1fr_1fr] gap-14 my-10 mt-40 text-sm py-5'>
            {/* Left */}
            <div>
                <img src={assets.logo} className='w-40 mb-3'></img>
                <p className='w-full md:w-2/3 text-gray-600 leading-6'>Your trusted partner for online doctor appointments and prescriptions.Built with using Python & MERN Stack.<br/>📍 India | 🌐 https://docprescops.space <br/> 📧 contact@docprescops.com</p>
            </div>

            {/* Center */}
            <div>
                <p className='text-xl font-medium mb-5 mt-2'>COMPANY</p>
                <ul className='flex flex-col gap-2 text-gray-600'>
                    <li><a href='/'>Home</a></li>
                    <li><a href='/about'>About us</a></li>  
                    <li><a href='/contact'>Contact us</a></li>
                    <li><a href='/privacy'>Privacy policy</a></li>
                </ul>
            </div>

            {/* Right */}
            <div>
                <p className='text-xl font-medium mb-5 mt-2'>GET IN TOUCH</p>
                <ul className='flex flex-col gap-2 text-gray-600'>
                    <li>+91 8156040130</li>
                    <li>contact@docprescops.com</li>
                </ul>
            </div>
        </div>
        <div>
            {/* Copyright */}
            <hr></hr>
            <p className='py-5 text-sm text-center'>Copyright © 2026 Docprescops - All Right Reserved.</p>
        </div>
    </div>
    </div>

  )
}

export default Footer
