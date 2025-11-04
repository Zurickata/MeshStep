/**************************************************************************/
/*                                                                        */
/*                  Jens                                                  */
/*                                                                        */
/**************************************************************************/
/* Allows to display Jacobian Information of a mesh in .m3d format        */
/* Written by Claudio Lobos (clobos@inf.utfsm.cl) 2015					  */
/* UNIVERSIDAD TECNICA FEDERICO SANTA MARIA								  */
/**************************************************************************/

/*
 <JENS: this program computes the Element Normalized Scaled Jacobian (Jens)>
 
 Copyright (C) <2015>  <Claudio Lobos>
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/gpl.txt>
 */


#ifndef Elementr_h
#define Elementr_h 1

#include <string>
#include <cctype>
#include <iostream>
#include <list>
#include <math.h>
#include "Point3D.h"
#include "math/Matrix.h"
#include "math/Polynom.h"
#include <limits>
//#include "FaceContainer.h"

using Clobscode::Point3D;

using namespace std;

class Element {
    
public:
    
    Element();
    
    Element(vector<int> &pts);
    
    virtual ~Element();
    
    virtual vector<unsigned int> &getPoints();
    
    virtual double getAspectRatio(vector<Point3D> &points)=0;

    virtual double getEdgeAspectRatio(vector<Point3D> &points);
    
    virtual double getElementJS(vector<Point3D> &points);

    virtual double getElementJENS(vector<Point3D> &points);

    virtual double getElementJEANS(vector<Point3D> &points);
    
    virtual double getElementJRATIO(vector<Point3D> &points);
                                
    virtual vector<double> getJS(vector<Point3D> &points);
    
    virtual vector<double> getJENS(vector<Point3D> &points);

    virtual vector<double> getJEANS(vector<Point3D> &points);
    
    virtual vector<double> getJRatios(vector<Point3D> &points)=0;
    
    virtual char getCharType();
    
    friend std::ostream& operator<<(std::ostream& o, Element &e);
    
    virtual void computeBbox(vector<Point3D> &coords);
    
    virtual vector<unsigned int> getFacePoints(const unsigned int &i)=0;
    
    virtual unsigned int numberOfFaces()=0;
    
     bool surfaceElement = false;
    
    //memorist
    
    //virtual void printer(FaceContainer &fc, FaceContainer &sfc);
    
     //virtual void ESChecker(FaceContainer &fc, FaceContainer &sfc);
    
    
    virtual void addFace(unsigned int idx);
    
    virtual list<unsigned int> &getFaces();
    
    virtual void remove(int axe, double start, double end);
    
    virtual bool wasRemoved();

    virtual double getJeansConstant() const;
    
    friend std::ostream& operator<<(std::ostream& o, Element &e);
    //friend std::ostream& operator<<(std::ostream& o, const Element &e);
    //--
    list<unsigned int> faces;

protected:
    
    virtual vector<double> getJENSConstant();
    
    virtual vector<unsigned int> getTetra(int index)=0;
    
    virtual vector<vector<unsigned int> > getTetras()=0;
    
    vector<unsigned int> points;
	vector<double> jens_constant;
    double js, jens, jeans_constant;
    char type;
    vector<Point3D> rst;
    vector<Point3D> grst;
    
    //memorist
    
    string color;
    //string type;
    bool colored,removed;
    Point3D min, max;
    //--
    
};
//memorist

inline double Element::getJeansConstant() const {
    return jeans_constant;
}

inline void Element::addFace(unsigned int idx) {
    faces.push_back(idx);
}

inline list<unsigned int> &Element::getFaces() {
    return faces;
}

inline bool Element::wasRemoved(){
    return removed;
}

//--

inline vector<double> Element::getJENSConstant() {
    return jens_constant;
}

inline vector<unsigned int> &Element::getPoints(){
    return points;
}

inline char Element::getCharType(){
    return type;
}

#endif

