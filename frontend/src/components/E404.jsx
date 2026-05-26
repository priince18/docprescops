import React from 'react'
import { assets } from '../assets/assets'

const E404 = () => {
  return (
  
    <div className='md:mx-11 '>
        <div className='flex justify-center mt-10'>
            <img src={assets.error_img} alt="404 Error" className='w-1/2 md:w-1/3' />
        </div>

        <h1 className='text-6xl font-bold text-center'>404</h1>

        <p className='text-xl text-center mt-4 text-gray-600'>Page Not Found</p>

        <div className='flex justify-center mt-10'>
            <a href='/' className='bg-primary hover:bg-pg text-white px-6 py-3 rounded-full hover:scale-105 transition-all duration-300'>Go Back Home</a>
        </div>
    </div>

  )
}

export default E404
