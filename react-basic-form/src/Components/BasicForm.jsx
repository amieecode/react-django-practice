import React, { useState } from 'react'

const BasicForm = () => {
    const [formData, setFormData] = useState({ name: '', email: ''});
    
    const handleChange = (e)=> {
      const { name, value } = e.target;
      setFormData({ ...formData, [name]: value });
    }

    const handleSubmit = (e) =>{
        e.preventDefault();
        console.log('formDate:', formData)
    }

  return (
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input type="text" name='name' value={formData.value} onChange={handleChange} />
        </div>
        <div>
          <label>Email</label>
          <input type="text" name='email' value={formData.value} onChange={handleChange} />  
        </div>

        <button type='submit'>Submit</button>
      </form>
  )
}

export default BasicForm;
