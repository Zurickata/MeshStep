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
 <JENS: this program computes the Metric Normalized Scaled Jacobian (Jens)>
 
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


#ifndef Metricr_h
#define Metricr_h 1

#include "Element.h"
#include "Point3D.h"
#include <vector>

using Clobscode::Point3D;

using namespace std;

class Metric {
    
public:
    
    Metric();
    
    virtual ~Metric();
    
    virtual vector<double> getNodeQuality(Element *element, vector<Point3D> &points)=0;

    virtual double getElementQuality(Element *element, vector<Point3D> &points)=0;
	
	/*protected:
	
	vector<Point3D> points;*/

};

#endif

