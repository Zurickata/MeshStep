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

#include "Hexahedron.h"


//---------------------------------------------------------------//
//---------------------------------------------------------------//
Hexahedron::Hexahedron(vector<int> &pts):Element(pts) {
    type = 'H';
    jens_constant.assign(8,1.0);
    jeans_constant = 1.0;
    
    //reference coordinates for referential hexahedron.
    rst.reserve(8);
    rst.push_back(Point3D (-1,-1,1));
    rst.push_back(Point3D (1,-1,1));
    rst.push_back(Point3D (1,-1,-1));
    rst.push_back(Point3D (-1,-1,-1));
    rst.push_back(Point3D (-1,1,1));
    rst.push_back(Point3D (1,1,1));
    rst.push_back(Point3D (1,1,-1));
    rst.push_back(Point3D (-1,1,-1));
    
    grst.reserve(8);
    double g=1/sqrt(3);
	
	//uncomment the next line if you want to compute 
	//the JR at corner nodes
	//g = 1;
    
    grst.push_back(Point3D (-g,-g,g));
    grst.push_back(Point3D (g,-g,g));
    grst.push_back(Point3D (g,-g,-g));
    grst.push_back(Point3D (-g,-g,-g));
    
    grst.push_back(Point3D (-g,g,g));
    grst.push_back(Point3D (g,g,g));
    grst.push_back(Point3D (g,g,-g));
    grst.push_back(Point3D (-g,g,-g));
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
Hexahedron::~Hexahedron(){
    
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Hexahedron::getAspectRatio(vector<Point3D> &points) {
    return 0;
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Hexahedron::getJRatios(vector<Point3D> &points) {
    vector<double> jrats(8,0);
    double max = -std::numeric_limits<double>::max();
    for (int i=0; i<8; i++) {
        jrats[i] = getDet(points, grst[i]);
        double pos = fabs(jrats[i]);
        if (max<pos) {
            max = pos;
        }
    }

    for (unsigned int i=0; i<8; i++) {
        jrats[i]/=max;
    }
    return jrats;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Hexahedron::getElementJENS(vector<Point3D> &pts)
{

    // IMPORTANT NOTE: For the case of Hexahedron this method is
    // redefined for an optimization (its Jens constant is 1).

    double worst = 2;

    vector<vector<unsigned int>> tets = getTetras();

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        v0.normalize();
        v1.normalize();
        v2.normalize();
        double q = (v0.cross(v1)).dot(v2);

        if (q < worst)
        {
            worst = q;
        }
    }

    return worst;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Hexahedron::getJENS(vector<Point3D> &pts)
{

    vector<vector<unsigned int>> tets = getTetras();
    vector<double> jens(tets.size(), 0);

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        v0.normalize();
        v1.normalize();
        v2.normalize();

        jens[i] = (v0.cross(v1)).dot(v2);

    }

    return jens;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Hexahedron::getElementJEANS(vector<Point3D> &pts)
{
    double worst = 2;

    vector<vector<unsigned int>> tets = getTetras();

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        double length = 1;

        v0 /= length;
        v1 /= length;
        v2 /= length;

        double q = (v0.cross(v1)).dot(v2);

        if (q < worst)
        {
            worst = q;
        }
    }

    return worst;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Hexahedron::getJEANS(vector<Point3D> &pts)
{
    vector<vector<unsigned int>> tets = getTetras();
    vector<double> jeans(tets.size(), 0);

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        double length = 1;

        v0 /= length;
        v1 /= length;
        v2 /= length;

        jeans[i] = (v0.cross(v1)).dot(v2);

    }

    return jeans;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Hexahedron::getDet(vector<Point3D> &pts, const Point3D &p){
    
    double r = p[0], s = p[1], t = p[2];
    CMatrix coef, hex;
    static bool init = false;
    static CMatrix invhex;
    
    if(!init){
        hex.SetDims(8,8);
        
        for(int j=0;j<8;j++){
            hex.Elt(0,j)=rst[j][0];
            hex.Elt(1,j)=rst[j][1];
            hex.Elt(2,j)=rst[j][2];
            hex.Elt(3,j)=rst[j][0]*rst[j][1];
            hex.Elt(4,j)=rst[j][0]*rst[j][2];
            hex.Elt(5,j)=rst[j][1]*rst[j][2];
            hex.Elt(6,j)=rst[j][0]*rst[j][1]*rst[j][2];
            hex.Elt(7,j)=1;
        }
        
        hex.CF_InverseTo(invhex);
        
        init = true;
    }
    
    CMatrix mpoints;
    mpoints.SetDims(3,8);
    for(int j=0;j<8;j++){
        //if local points provided, use points[j] instead of points[idx[j]]
        Point3D mp = pts[points[j]];
        mpoints.Elt(0,j) = mp[0];
        mpoints.Elt(1,j) = mp[1];
        mpoints.Elt(2,j) = mp[2];
    }
    mpoints.Mult(invhex,coef);
    
    CPolynom xyz[3];
    for(int i=0;i<3;i++){
        xyz[i] = coef.Elt(i,0)*_X_ + coef.Elt(i,1)*_Y_ + coef.Elt(i,2)*_Z_ +
        coef.Elt(i,3)*_XY_ + coef.Elt(i,4)*_XZ_ + coef.Elt(i,5)*_YZ_ +
        coef.Elt(i,6)*_XYZ_ + coef.Elt(i,7);
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
vector<vector<unsigned int> > Hexahedron::getTetras() {
    
    vector<vector<unsigned int> > tets;
    tets.reserve(8);
    
    vector<unsigned int> t0(4,0);
    t0[0]=points[0];
    t0[1]=points[1];
    t0[2]=points[3];
    t0[3]=points[4];
    tets.push_back(t0);
    
    vector<unsigned int> t1(4,0);
    t1[0]=points[1];
    t1[1]=points[2];
    t1[2]=points[0];
    t1[3]=points[5];
    tets.push_back(t1);
    
    vector<unsigned int> t2(4,0);
    t2[0]=points[2];
    t2[1]=points[3];
    t2[2]=points[1];
    t2[3]=points[6];
    tets.push_back(t2);
    
    vector<unsigned int> t3(4,0);
    t3[0]=points[3];
    t3[1]=points[0];
    t3[2]=points[2];
    t3[3]=points[7];
    tets.push_back(t3);
    
    vector<unsigned int> t4(4,0);
    t4[0]=points[4];
    t4[1]=points[7];
    t4[2]=points[5];
    t4[3]=points[0];
    tets.push_back(t4);
    
    vector<unsigned int> t5(4,0);
    t5[0]=points[5];
    t5[1]=points[4];
    t5[2]=points[6];
    t5[3]=points[1];
    tets.push_back(t5);
    
    vector<unsigned int> t6(4,0);
    t6[0]=points[6];
    t6[1]=points[5];
    t6[2]=points[7];
    t6[3]=points[2];
    tets.push_back(t6);
    
    vector<unsigned int> t7(4,0);
    t7[0]=points[7];
    t7[1]=points[6];
    t7[2]=points[4];
    t7[3]=points[3];
    tets.push_back(t7);
    
    return tets;
}


//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<unsigned int> Hexahedron::getTetra(int index){
    
    vector<unsigned int> t(4,0);
    
    if(index == 0){
        t[0]=points[0];
        t[1]=points[1];
        t[2]=points[3];
        t[3]=points[4];
    }
    else if(index==1){
        t[0]=points[1];
        t[1]=points[2];
        t[2]=points[0];
        t[3]=points[5];
    }
    else if(index==2){
        t[0]=points[2];
        t[1]=points[3];
        t[2]=points[1];
        t[3]=points[6];
    }
    else if(index==3){
        t[0]=points[3];
        t[1]=points[0];
        t[2]=points[2];
        t[3]=points[7];
    }
    else if(index==4){
        t[0]=points[4];
        t[1]=points[7];
        t[2]=points[5];
        t[3]=points[0];
    }
    else if(index==5){
        t[0]=points[5];
        t[1]=points[4];
        t[2]=points[6];
        t[3]=points[1];
    }
    else if(index==6){
        t[0]=points[6];
        t[1]=points[5];
        t[2]=points[7];
        t[3]=points[2];
    }
    else if(index==7){
        t[0]=points[7];
        t[1]=points[6];
        t[2]=points[4];
        t[3]=points[3];
    }
    
    return t;
}

//memorist
vector<unsigned int> Hexahedron::getFacePoints(const unsigned int &index){
    vector<unsigned int> aux;
    aux.reserve(4);
    switch(index){
        case 0:
            aux.push_back(points[0]);
            aux.push_back(points[3]);
            aux.push_back(points[2]);
            aux.push_back(points[1]);
            break;
        case 1:
            aux.push_back(points[0]);
            aux.push_back(points[1]);
            aux.push_back(points[5]);
            aux.push_back(points[4]);
            break;
        case 2:
            aux.push_back(points[1]);
            aux.push_back(points[2]);
            aux.push_back(points[6]);
            aux.push_back(points[5]);
            break;
        case 3:
            aux.push_back(points[2]);
            aux.push_back(points[3]);
            aux.push_back(points[7]);
            aux.push_back(points[6]);
            break;
        case 4:
            aux.push_back(points[3]);
            aux.push_back(points[0]);
            aux.push_back(points[4]);
            aux.push_back(points[7]);
            break;
        case 5:
            aux.push_back(points[4]);
            aux.push_back(points[5]);
            aux.push_back(points[6]);
            aux.push_back(points[7]);
            break;
        default:
            break;
    }
    return aux;
}
//--
