
import './Hover.css';
import { ReactComponent as Avatar } from './Edy.svg';

const Hover = ({onClose}) => {
return (
    <div className="chat-popup">
      <Avatar className="edy-avatar" />
      <div className="avatar-msg">
        Welcome to EdMyst! My name is Edy. How can I help you?
      </div>
      
    </div>
  );
};
   
export default Hover;