import { useState } from "react"

const CounterApp = () => {
    const [count, setCount] = useState(0);

  return (
    <div className={styles.container}>
      <h1> Simple Counter App</h1> 
      <p>Current Count: {count} </p> 
      <div className={styles.groupButton}>
        <button style={styles.button} onClick={() => setCount(count + 1)}>Increase</button>
        <button style={styles.button} onClick={() => setCount(count - 1)}>Decrease</button>
        <button style={styles.button} onClick={() => setCount(0)}>Reset</button>
      </div>
    </div>
  )
}

// Inline styles (optional — you can use CSS instead)
const styles = {
    container: {
      textAlign: 'center',
      marginTop: '50px',
      fontFamily: 'Arial, sans-serif',
    },
    buttonGroup: {
      marginTop: '20px',
    },
    button: {
      margin: '5px',
      padding: '10px 20px',
      fontSize: '16px',
      cursor: 'pointer',
    }
  };
  
export default CounterApp;
