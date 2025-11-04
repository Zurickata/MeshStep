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

#ifndef Quality_h
#define Quality_h 1

#include "Hexahedron.h"
#include "Prism.h"
#include "Pyramid.h"
#include "Tetrahedron.h"
#include "Point3D.h"
#include "Metric.h"

using namespace std;

class Quality {
    
public:
    Quality();
    
    virtual ~Quality();

    virtual void executeGeneralStatistics(vector<Point3D> &points, vector<Element *> &elements, Metric *metric);
    
    /*virtual void execute_JS(vector<Point3D> &points, vector<Element *> &elements);
    
    virtual void execute_JENS(vector<Point3D> &points, vector<Element *> &elements);

    virtual void execute_JEANS(vector<Point3D> &points, vector<Element *> &elements);*/

    virtual void execute_JENS_Worst(vector<Point3D> &points, vector<Element *> &elements);
    
    virtual void execute_all(vector<Point3D> &points, vector<Element *> &elements);
    
    virtual void execute_allAR(vector<Point3D> &points, vector<Element *> &elements);

    virtual void execute_allJENS(vector<Point3D> &points, vector<Element *> &elements);

    virtual void execute_compareJensAndJeans(vector<Point3D> &points, vector<Element *> &elements);
    
};

#endif

