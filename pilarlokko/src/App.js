import React, { Component } from 'react';
import { HashRouter, Switch, Route } from 'react-router-dom';

import Header from './components/Header';
import Footer from './components/Footer';
import LandingPage from './components/LandingPage';
import Newsletter from './components/Newsletter';
import Contact from './components/Contact';
import NotFound from './components/NotFound';


class App extends Component {

    render() {
        return(
            <HashRouter basename={process.env.PUBLIC_URL}>
                <div className='Site'>
                    <div className='Site-content'>
                        <Header />
                        <Switch>
                            <Route exact path={process.env.PUBLIC_URL + '/'} component={LandingPage} />
                            <Route path={process.env.PUBLIC_URL + '/newsletter'} component={Newsletter} />
                            <Route path={process.env.PUBLIC_URL + '/contact'} component={Contact} />
                            <Route component={NotFound} />
                        </Switch>
                    </div>
                    <Footer theme='main' />
                </div>
            </HashRouter>
        )
    }
}

export default App;
