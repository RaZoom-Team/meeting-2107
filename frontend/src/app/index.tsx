import { createRoot } from 'react-dom/client'
import {App} from './ui/app.tsx'
import './index.scss'
import UserProvider from './providers/userProvider.tsx'
import '@gravity-ui/uikit/styles/fonts.css';
import '@gravity-ui/uikit/styles/styles.css';

createRoot(document.getElementById('root')!).render(
        <UserProvider>
            <App/>
        </UserProvider>
)


