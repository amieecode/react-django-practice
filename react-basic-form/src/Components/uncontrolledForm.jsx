import { useRef } from "react";

const UncontrolledForm = () => {
    const inputRef = useRef();

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log("Submitted name:", inputRef.current.value)
    }
  return (
    <form onSubmit={handleSubmit}>
      <input type="text" ref={inputRef}/>
      <button type='submit'>Submit</button>
    </form>
  )
}

export default UncontrolledForm;
