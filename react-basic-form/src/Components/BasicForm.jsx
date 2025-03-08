import React from 'react'

const BasicForm = () => {
    const handleSubmit = (event) =>{
        event.preventDefault();
        console.log('form Submitted')
    }

  return (
    <div>
      <form onClick={handleSubmit}>
        <button type='submit'>Submit</button>
      </form>
    </div>
  )
}

export default BasicForm;
