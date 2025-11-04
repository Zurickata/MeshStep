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

#include "Tetrahedron.h"


//---------------------------------------------------------------//
//---------------------------------------------------------------//
Tetrahedron::Tetrahedron(vector<int> &pts):Element(pts) {
    type='T';
    jens_constant.assign(4,1.0/sqrt(2));

    jeans_constant = 1.0;
    
    rst.reserve(4);
    rst.push_back(Point3D (-1,-1,-1));
    rst.push_back(Point3D (-1,-1,1));
    rst.push_back(Point3D (1,-1,1));
    rst.push_back(Point3D (-1,1,-1));

    
    grst.reserve(4);
    double g=1/sqrt(3);
	
	//uncomment the next line if you want to compute 
	//the JR at corner nodes
	//g = 1;
	
    grst.push_back(Point3D (-g,-g,-g));
    grst.push_back(Point3D (-g,-g,g));
    grst.push_back(Point3D (g,-g,g));
    grst.push_back(Point3D (-g,g,-g));

    
}

Tetrahedron::~Tetrahedron(){
    
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Tetrahedron::getJRatios(vector<Point3D> &pts) {
    vector<double> jrats(4,1);
    double max = -std::numeric_limits<double>::max();
    for (int i=0; i<4; i++) {
        jrats[i] = getDet(pts,grst[i]);
        double pos = fabs(jrats[i]);
        if (max<pos) {
            max = pos;
        }
    }

    for (int i=0; i<4; i++) {
        jrats[i]/=max;
    }
    return jrats;
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Tetrahedron::getDet(vector<Point3D> &pts, const Point3D &p){
    
    double r = p[0], s = p[1], t = p[2];
    CMatrix coef, tet;
    static bool init = false;
    static CMatrix invtet;
    
    if(!init){
        tet.SetDims(4,4);
        
        for(int j=0;j<4;j++){
            tet.Elt(0,j)=rst[j][0];
            tet.Elt(1,j)=rst[j][1];
            tet.Elt(2,j)=rst[j][2];
            tet.Elt(3,j)=1;
        }
        
        tet.CF_InverseTo(invtet);
        init = true;
    }
    
    CMatrix mpoints;
    mpoints.SetDims(3,4);
    for(int j=0;j<4;j++){
        Point3D mp = pts[points[j]];
        mpoints.Elt(0,j) = mp[0];
        mpoints.Elt(1,j) = mp[1];
        mpoints.Elt(2,j) = mp[2];
    }
    
    mpoints.Mult(invtet,coef);
    
    CPolynom xyz[3];
    for(int i=0;i<3;i++){
        xyz[i] = coef.Elt(i,0)*_X_ + coef.Elt(i,1)*_Y_ +
        coef.Elt(i,2)*_Z_ + coef.Elt(i,3);
    }
    
    CMatrix jacques;
    
    jacques.SetDims(3,3);
    for(int j=0;j<3;j++){
        jacques.Elt(0,j) = xyz[j].DerX().EvalAt(r,s,t);
        jacques.Elt(1,j) = xyz[j].DerY().EvalAt(r,s,t);
        jacques.Elt(2,j) = xyz[j].DerZ().EvalAt(r,s,t);
    }
    
    return jacques.CF_Det();
    
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
void Tetrahedron::getPointsIndexInEdge(int index, int &pindex1,
                                       int &pindex2){
    
    if(index<0 || index>5)
        return;
    switch(index){
        case 0:
            pindex1=points[0];
            pindex2=points[1];
            break;
        case 1:
            pindex1=points[2];
            pindex2=points[0];
            break;
        case 2:
            pindex1=points[3];
            pindex2=points[0];
            break;
        case 3:
            pindex1=points[1];
            pindex2=points[2];
            break;
        case 4:
            pindex1=points[3];
            pindex2=points[1];
            break;
        case 5:
            pindex1=points[3];
            pindex2=points[2];
            break;
        default:
            return;
    }
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Tetrahedron::getAspectRatio(vector<Point3D> &points) {

    int eip1,eip2;
    Point3D p1,p2,p;
    double aspectratio = 0;
    
    for(int i=0;i<6;i++){
        getPointsIndexInEdge(i,eip1,eip2);
        p1 = points[eip1];
        p2 = points[eip2];
        p = p1-p2;
        aspectratio += p.dot(p);
    }
    
    aspectratio /= 6;
    aspectratio = pow(aspectratio,1.5);
    aspectratio /= 8.48528*getVolume(points);
    return 1/aspectratio;
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Tetrahedron::getVolume(vector<Point3D> &pts){
    Point3D v1,v2,v3,v4,dif1,dif2,dif3,crossr;
    double vol;
    
    v1=pts[points[0]];
    v2=pts[points[1]];
    v3=pts[points[2]];
    v4=pts[points[3]];
    dif1=v2-v1;
    dif2=v3-v1;
    dif3=v4-v1;
    crossr=dif1.cross(dif2);
    vol=(dif3.dot(crossr));
    return vol/6;
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<vector<unsigned int> > Tetrahedron::getTetras() {
    
    /*note: due to vector noramlization, the value of JENS
     is not the same for every node, therfore we need to compute
     the quality for each node. This is a different behavior from
     Jacobian computation*/
    
    vector<vector<unsigned int> > tetras;
    tetras.reserve(4);
    
    vector<unsigned int> t0(4,0);
    t0[0]= points[0];
    t0[1]= points[1];
    t0[2]= points[2];
    t0[3]= points[3];
    tetras.push_back(t0);
    
    vector<unsigned int> t1(4,0);
    t1[0]= points[1];
    t1[1]= points[2];
    t1[2]= points[0];
    t1[3]= points[3];
    tetras.push_back(t1);
    
    vector<unsigned int> t2(4,0);
    t2[0]= points[2];
    t2[1]= points[0];
    t2[2]= points[1];
    t2[3]= points[3];
    tetras.push_back(t2);
    
    vector<unsigned int> t3(4,0);
    t3[0]= points[3];
    t3[1]= points[2];
    t3[2]= points[1];
    t3[3]= points[0];
    tetras.push_back(t3);
    
    return tetras;
}

//memorist
vector<unsigned int> Tetrahedron::getFacePoints(const unsigned int &index){
    
    vector<unsigned int> aux;
    aux.reserve(3);
    
    switch(index){
        case 0:
            aux.push_back(points[0]);
            aux.push_back(points[2]);
            aux.push_back(points[1]);
            break;
        case 1:
            aux.push_back(points[0]);
            aux.push_back(points[1]);
            aux.push_back(points[3]);
            break;
        case 2:
            aux.push_back(points[1]);
            aux.push_back(points[2]);
            aux.push_back(points[3]);
            break;
        case 3:
            aux.push_back(points[2]);
            aux.push_back(points[0]);
            aux.push_back(points[3]);
            break;
        default:
            break;
    }
    return aux;
}
//--
