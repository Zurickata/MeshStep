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

#include "Prism.h"

//---------------------------------------------------------------//
//---------------------------------------------------------------//
Prism::Prism(vector<int> &pts) : Element(pts)
{
    type = 'R';
    jens_constant.assign(6, sqrt(0.75)); // sqrt(3)/2 = sqrt(0.75)
    jeans_constant = sqrt(1.5);          // sqrt(6)/2 = sqrt(6/4) = sqrt(3/2)

    rst.reserve(6);
    rst.clear();

    rst.push_back(Point3D(-1, -1, -1));
    rst.push_back(Point3D(1, -1, -1));
    rst.push_back(Point3D(-1, 1, -1));
    rst.push_back(Point3D(-1, -1, 1));
    rst.push_back(Point3D(1, -1, 1));
    rst.push_back(Point3D(-1, 1, 1));

    grst.reserve(8);
    double g = 1 / sqrt(3);

    // uncomment the next line if you want to compute
    // the JR at corner nodes
    // g = 1;

    grst.push_back(Point3D(-g, -g, -g));
    grst.push_back(Point3D(g, -g, -g));
    grst.push_back(Point3D(-g, g, -g));
    grst.push_back(Point3D(-g, -g, g));
    grst.push_back(Point3D(g, -g, g));
    grst.push_back(Point3D(-g, g, g));
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
Prism::~Prism()
{
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Prism::getAspectRatio(vector<Point3D> &points)
{
    return 0;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Prism::getDet(vector<Point3D> &pts, const Point3D &p)
{

    double r = p[0], s = p[1], t = p[2];
    CMatrix coef, prism;
    static bool init = false;
    static CMatrix invprism;

    if (!init)
    {
        prism.SetDims(6, 6);

        for (int j = 0; j < 6; j++)
        {
            prism.Elt(0, j) = rst[j][0];
            prism.Elt(1, j) = rst[j][1];
            prism.Elt(2, j) = rst[j][2];
            prism.Elt(3, j) = rst[j][0] * rst[j][2];
            prism.Elt(4, j) = rst[j][1] * rst[j][2];
            prism.Elt(5, j) = 1;
        }

        prism.CF_InverseTo(invprism);
        init = true;
    }

    CMatrix mpoints;
    mpoints.SetDims(3, 6);
    for (int j = 0; j < 6; j++)
    {
        Point3D mp = pts[points[j]];
        mpoints.Elt(0, j) = mp[0];
        mpoints.Elt(1, j) = mp[1];
        mpoints.Elt(2, j) = mp[2];
    }

    mpoints.Mult(invprism, coef);

    CPolynom xyz[3];
    for (int i = 0; i < 3; i++)
    {
        xyz[i] = coef.Elt(i, 0) * _X_ + coef.Elt(i, 1) * _Y_ +
                 coef.Elt(i, 2) * _Z_ + coef.Elt(i, 3) * _XZ_ +
                 coef.Elt(i, 4) * _YZ_ + coef.Elt(i, 5);
    }

    CMatrix jacques;

    jacques.SetDims(3, 3);
    for (int j = 0; j < 3; j++)
    {
        jacques.Elt(0, j) = xyz[j].DerX().EvalAt(r, s, t);
        jacques.Elt(1, j) = xyz[j].DerY().EvalAt(r, s, t);
        jacques.Elt(2, j) = xyz[j].DerZ().EvalAt(r, s, t);
    }

    return jacques.CF_Det();
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Prism::getElementJEANS(vector<Point3D> &pts)
{

    double worst = 2;

    vector<vector<unsigned int>> tets = getTetras();

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        v0 /= jeans_constant;
        v1 /= jeans_constant;

        double length = 1;

        v0 /= length;
        v1 /= length;
        v2 /= length;

        double q = (v0.cross(v1)).dot(v2);

        if (q > jens_constant[i])
        {
            q = 1 + jens_constant[i] - q;
        }
        else
        {
            if (q < (jens_constant[i] * -1))
            {
                q = -1 - jens_constant[i] - q;
            }
            else
            {
                q = q / jens_constant[i];
            }
        }

        if (q < worst)
        {
            worst = q;
        }
    }

    return worst;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Prism::getJEANS(vector<Point3D> &pts)
{

    vector<vector<unsigned int>> tets = getTetras();
    vector<double> jeans(tets.size(), 0);

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        v0 /= jeans_constant;
        v1 /= jeans_constant;

        double length = 1;

        v0 /= length;
        v1 /= length;
        v2 /= length;

        double q = (v0.cross(v1)).dot(v2);

        if (q > jens_constant[i])
        {
            q = 1 + jens_constant[i] - q;
        }
        else
        {
            if (q < (jens_constant[i] * -1))
            {
                q = -1 - jens_constant[i] - q;
            }
            else
            {
                q = q / jens_constant[i];
            }
        }

        jeans[i] = q;
    }

    return jeans;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Prism::getJRatios(vector<Point3D> &pts)
{
    vector<double> jrats(6, 0);
    double max = -std::numeric_limits<double>::max();

    for (int i = 0; i < 6; i++)
    {
        jrats[i] = getDet(pts, grst[i]);
        double pos = fabs(jrats[i]);
        if (max < pos)
        {
            max = pos;
        }
    }

    for (unsigned int i = 0; i < 6; i++)
    {
        jrats[i] /= max;
    }

    return jrats;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<vector<unsigned int>> Prism::getTetras()
{

    vector<vector<unsigned int>> tets;
    tets.reserve(6);

    /*Note: this order is stablished so in position 0 is the
      current node. In positions 1 and 2 will be the neighbors
      in the triangular face in a way that node 3 will be
      correctly positioned following the right hand rule.
      This is crucial to correctly compute JEANS metric.
    */
    vector<unsigned int> t0(4, 0);
    t0[0] = points[0];
    t0[1] = points[1];
    t0[2] = points[2];
    t0[3] = points[3];
    tets.push_back(t0);

    vector<unsigned int> t1(4, 0);
    t1[0] = points[1];
    t1[1] = points[2];
    t1[2] = points[0];
    t1[3] = points[4];
    tets.push_back(t1);

    vector<unsigned int> t2(4, 0);
    t2[0] = points[2];
    t2[1] = points[0];
    t2[2] = points[1];
    t2[3] = points[5];
    tets.push_back(t2);

    vector<unsigned int> t3(4, 0);
    t3[0] = points[3];
    t3[1] = points[5];
    t3[2] = points[4];
    t3[3] = points[0];
    tets.push_back(t3);

    vector<unsigned int> t4(4, 0);
    t4[0] = points[4];
    t4[1] = points[3];
    t4[2] = points[5];
    t4[3] = points[1];
    tets.push_back(t4);

    vector<unsigned int> t5(4, 0);
    t5[0] = points[5];
    t5[1] = points[4];
    t5[2] = points[3];
    t5[3] = points[2];

    tets.push_back(t5);

    return tets;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<unsigned int> Prism::getTetra(int index)
{

    /*Note: this order is stablished so in position 0 is the
      current node. In positions 1 and 2 will be the neighbors
      in the triangular face in a way that node 3 will be
      correctly positioned following the right hand rule.
      This is crucial to correctly compute JEANS metric.
    */
    vector<unsigned int> t(4, 0);
    if (index == 0)
    {
        t[0] = points[0];
        t[1] = points[1];
        t[2] = points[2];
        t[3] = points[3];
    }
    else if (index == 1)
    {
        t[0] = points[1];
        t[1] = points[2];
        t[2] = points[0];
        t[3] = points[4];
    }
    else if (index == 2)
    {
        t[0] = points[2];
        t[1] = points[0];
        t[2] = points[1];
        t[3] = points[5];
    }
    else if (index == 3)
    {
        t[0] = points[3];
        t[1] = points[5];
        t[2] = points[4];
        t[3] = points[0];
    }
    else if (index == 4)
    {
        t[0] = points[4];
        t[1] = points[3];
        t[2] = points[5];
        t[3] = points[1];
    }
    else if (index == 5)
    {
        t[0] = points[5];
        t[1] = points[4];
        t[2] = points[3];
        t[3] = points[2];
    }

    return t;
}

// memorist
vector<unsigned int> Prism::getFacePoints(const unsigned int &index)
{
    vector<unsigned int> aux;
    aux.reserve(4);
    switch (index)
    {
    case 0:
        aux.reserve(4);
        aux.push_back(points[0]);
        aux.push_back(points[1]);
        aux.push_back(points[4]);
        aux.push_back(points[3]);
        break;
    case 1:
        aux.reserve(4);
        aux.push_back(points[1]);
        aux.push_back(points[2]);
        aux.push_back(points[5]);
        aux.push_back(points[4]);
        break;
    case 2:
        aux.reserve(4);
        aux.push_back(points[0]);
        aux.push_back(points[3]);
        aux.push_back(points[5]);
        aux.push_back(points[2]);
        break;
    case 3:
        aux.reserve(3);
        aux.push_back(points[0]);
        aux.push_back(points[2]);
        aux.push_back(points[1]);
        break;
    case 4:
        aux.reserve(3);
        aux.push_back(points[3]);
        aux.push_back(points[4]);
        aux.push_back(points[5]);
        break;
    default:
        break;
    }
    return aux;
}
//--
