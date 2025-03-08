import {useState } from 'react'

const ControlledForm = () => {
    const [name, setName] = useState('');

    const handleChange = (event) => {
        setName(event.target.value);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('Submitted name:', name)
    }
  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={name} onChange={handleChange}/>
      <button type='submit'>Submit</button>
    </form>
  )
}

export default ControlledForm
