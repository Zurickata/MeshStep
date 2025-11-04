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

#include "Pyramid.h"

//---------------------------------------------------------------//
//---------------------------------------------------------------//
Pyramid::Pyramid(vector<int> &pts) : Element(pts)
{
    type = 'P';
    jens_constant.reserve(8);
    jens_constant.assign(4, sqrt(6) / 3.0);
    for (unsigned int i = 4; i < 8; i++)
    {
        jens_constant.push_back((sqrt(6) * 2.0) / 9.0);
    }

    jeans_constant = sqrt(2.0 / 3.0);

    // reference coordinates for pyramid seen as a degenerated
    // hexahedron where nodes 4 to 7 are the same.
    rst.reserve(8);

    rst.push_back(Point3D(-1, -1, 1));
    rst.push_back(Point3D(1, -1, 1));
    rst.push_back(Point3D(1, -1, -1));
    rst.push_back(Point3D(-1, -1, -1));

    rst.push_back(Point3D(-1, 1, 1));
    rst.push_back(Point3D(1, 1, 1));
    rst.push_back(Point3D(1, 1, -1));
    rst.push_back(Point3D(-1, 1, -1));

    // gauss reference coordinates for pyramide seen as a degenerated
    // hexahedron where nodes 4 to 7 are very clos to each other
    //(Jacobian values always expected to be be small.
    grst.reserve(8);
    double g = 1 / sqrt(3);

    // uncomment the next line if you want to compute
    // the JR at corner nodes
    // g = 1;

    grst.push_back(Point3D(-g, -g, g));
    grst.push_back(Point3D(g, -g, g));
    grst.push_back(Point3D(g, -g, -g));
    grst.push_back(Point3D(-g, -g, -g));

    grst.push_back(Point3D(-g, g, g));
    grst.push_back(Point3D(g, g, g));
    grst.push_back(Point3D(g, g, -g));
    grst.push_back(Point3D(-g, g, -g));
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
Pyramid::~Pyramid()
{
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Pyramid::getAspectRatio(vector<Point3D> &points)
{
    return 0;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Pyramid::getJRatios(vector<Point3D> &pts)
{

    vector<double> jrats(5, 0);
    double max = -2;

    /* Notes:
     - This method computes the jacobian at gauss points of an hexahedron.
       Therefore, for the apex there are 4 possible values usually close
       to cero values.
     - The constant values correspond to jacobian at gauss points of an
       equilateral pyramid. This is 0.055 for each base node and 0.004 for
       the values close to apex.
     */

    for (unsigned int i = 0; i < 4; i++)
    {
        jrats[i] = getDet(pts, grst[i]) / 0.0549783007034309;
    }

    // normalize JR value:
    jrats[4] = getDet(pts, grst[4]) / 0.00394726439544804;
    
    bool onepositive = false;
    if (jrats[4] > 0)
    {
        onepositive = true;
    }

    for (unsigned int i = 5; i < 8; i++)
    {
        // normalize JR value:
        double jr = getDet(pts, grst[i]) / 0.00394726439544804;
        ;
        if (onepositive)
        {

            /* We assign the worst among the 4 positive
               otherwise, it will always be one when all
               are positive
             */

            if (jr < jrats[4] && jr > 0)
            {
                jrats[4] = jr;
            }
        }
        else
        {
            if (jr >= 0)
            {
                onepositive = true;
                jrats[4] = jr;
            }
            else
            {
                if (jrats[4] > jr)
                {
                    jrats[4] = jr;
                }
            }
        }
    }

    for (unsigned int i = 0; i < 5; i++)
    {
        double pos = fabs(jrats[i]);
        if (max < pos)
        {
            max = pos;
        }
    }

    for (unsigned int i = 0; i < 5; i++)
    {
        jrats[i] /= max;
    }

    return jrats;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Pyramid::getDet(vector<Point3D> &pts, const Point3D &p)
{

    /* Computes the jacobian at point p, defined at the reference
     system: [-1,+1]^3. In other words p must be inside [-1,+1]^3
     */

    double r = p[0], s = p[1], t = p[2];
    CMatrix coef, hex;
    static bool init = false;
    static CMatrix invhex;

    if (!init)
    {
        hex.SetDims(8, 8);

        for (int j = 0; j < 8; j++)
        {
            hex.Elt(0, j) = rst[j][0];
            hex.Elt(1, j) = rst[j][1];
            hex.Elt(2, j) = rst[j][2];
            hex.Elt(3, j) = rst[j][0] * rst[j][1];
            hex.Elt(4, j) = rst[j][0] * rst[j][2];
            hex.Elt(5, j) = rst[j][1] * rst[j][2];
            hex.Elt(6, j) = rst[j][0] * rst[j][1] * rst[j][2];
            hex.Elt(7, j) = 1;
        }

        hex.CF_InverseTo(invhex);

        init = true;
    }

    CMatrix mpoints;
    mpoints.SetDims(3, 8);
    for (int j = 0; j < 4; j++)
    {
        Point3D p = pts[points[j]];
        mpoints.Elt(0, j) = p[0];
        mpoints.Elt(1, j) = p[1];
        mpoints.Elt(2, j) = p[2];
    }
    for (int j = 4; j < 8; j++)
    {
        Point3D p = pts[points[4]];
        mpoints.Elt(0, j) = p[0];
        mpoints.Elt(1, j) = p[1];
        mpoints.Elt(2, j) = p[2];
    }
    mpoints.Mult(invhex, coef);

    CPolynom xyz[3];
    for (int i = 0; i < 3; i++)
    {
        xyz[i] = coef.Elt(i, 0) * _X_ + coef.Elt(i, 1) * _Y_ +
                 coef.Elt(i, 2) * _Z_ + coef.Elt(i, 3) * _XY_ + coef.Elt(i, 4) * _XZ_ +
                 coef.Elt(i, 5) * _YZ_ + coef.Elt(i, 6) * _XYZ_ + coef.Elt(i, 7);
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
double Pyramid::getElementJS(vector<Point3D> &pts)
{

    double worst = 2;
    vector<double> auxjs = getJS(pts);

    for (unsigned int i = 0; i < auxjs.size(); i++)
    {
        if (worst > auxjs[i])
        {
            worst = auxjs[i];
        }
    }
    return worst;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Pyramid::getElementJENS(vector<Point3D> &pts)
{

    double worst = 2;
    vector<double> auxjens = getJENS(pts);

    for (unsigned int i = 0; i < auxjens.size(); i++)
    {
        if (worst > auxjens[i])
        {
            worst = auxjens[i];
        }
    }
    return worst;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Pyramid::getElementJEANS(vector<Point3D> &pts)
{

    double worst = 2;

    vector<vector<unsigned int>> tets = getTetras();

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        if (i < 4)
        {
            v0 /= jeans_constant;
            v1 /= jeans_constant;
        }

        double length = std::max({v0.Norm(), v1.Norm(), v2.Norm()});

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
vector<double> Pyramid::getJS(vector<Point3D> &pts)
{

    vector<double> auxjs, js(5, 0);

    auxjs = Element::getJS(pts);

    double minpos = 2, maxneg = -2, apice = 0;

    bool positive = false;

    for (unsigned int i = 4; i < auxjs.size(); i++)
    {
        if (auxjs[i] >= 0 && auxjs[i] < minpos)
        {
            minpos = auxjs[i];
            positive = true;
        }
        if (auxjs[i] < 0 && auxjs[i] > maxneg)
        {
            maxneg = auxjs[i];
        }
    }

    if (positive)
    {
        js[4] = minpos;
    }
    else
    {
        js[4] = maxneg;
    }

    for (unsigned int i = 0; i < 4; i++)
    {
        js[i] = auxjs[i];
    }

    return js;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Pyramid::getJENS(vector<Point3D> &pts)
{

    vector<double> auxjens, jens(5, 0);

    auxjens = Element::getJENS(pts);

    double minpos = 2, maxneg = -2, apice = 0;

    bool positive = false;

    for (unsigned int i = 0; i < 4; i++)
    {
        jens[i] = auxjens[i];
    }

    for (unsigned int i = 4; i < auxjens.size(); i++)
    {
        if (auxjens[i] >= 0 && auxjens[i] < minpos)
        {
            minpos = auxjens[i];
            positive = true;
        }
        if (auxjens[i] < 0 && auxjens[i] > maxneg)
        {
            maxneg = auxjens[i];
        }
    }

    if (positive)
    {
        jens[4] = minpos;
    }
    else
    {
        jens[4] = maxneg;
    }

    return jens;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Pyramid::getJEANS(vector<Point3D> &pts)
{

    vector<vector<unsigned int>> tets = getTetras();
    vector<double> jeans(5, 0);

    // Compute JEANS for basal face nodes.
    for (unsigned int i = 0; i < 4; i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        v0 /= jeans_constant;
        v1 /= jeans_constant;

        double length = std::max({v0.Norm(), v1.Norm(), v2.Norm()});

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

    // Compute JEANS for pyramid apex.

    double minpos = 2, maxneg = -2;
    bool positive = false;
    for (unsigned int i = 4; i < 8; i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        double length = std::max({v0.Norm(), v1.Norm(), v2.Norm()});

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

        if (q >= 0 && q < minpos)
        {
            minpos = q;
            positive = true;
        }
        if (q < 0 && q > maxneg)
        {
            maxneg = q;
        }
    }

    if (positive)
    {
        jeans[4] = minpos;
    }
    else
    {
        jeans[4] = maxneg;
    }

    return jeans;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<vector<unsigned int>> Pyramid::getTetras()
{

    vector<vector<unsigned int>> tets;
    tets.reserve(8);

    /*Note: this order is stablished so in position 0 is the
      current node. In positions 1 and 2 will be the neighbors
      in the triangular face in a way that node 3 will be
      correctly positioned following the right hand rule.
      This is crucial to correctly compute JEANS metric.
    */
    vector<unsigned int> t0(4, 0);
    t0[0] = points[0];
    t0[1] = points[1];
    t0[2] = points[3];
    t0[3] = points[4];
    tets.push_back(t0);

    vector<unsigned int> t1(4, 0);
    t1[0] = points[1];
    t1[1] = points[2];
    t1[2] = points[0];
    t1[3] = points[4];
    tets.push_back(t1);

    vector<unsigned int> t2(4, 0);
    t2[0] = points[2];
    t2[1] = points[3];
    t2[2] = points[1];
    t2[3] = points[4];
    tets.push_back(t2);

    vector<unsigned int> t3(4, 0);
    t3[0] = points[3];
    t3[1] = points[0];
    t3[2] = points[2];
    t3[3] = points[4];
    tets.push_back(t3);

    vector<unsigned int> t4(4, 0);
    t4[0] = points[4];
    t4[1] = points[0];
    t4[2] = points[3];
    t4[3] = points[1];
    tets.push_back(t4);

    vector<unsigned int> t5(4, 0);
    t5[0] = points[4];
    t5[1] = points[1];
    t5[2] = points[0];
    t5[3] = points[2];
    tets.push_back(t5);

    vector<unsigned int> t6(4, 0);
    t6[0] = points[4];
    t6[1] = points[2];
    t6[2] = points[1];
    t6[3] = points[3];
    tets.push_back(t6);

    vector<unsigned int> t7(4, 0);
    t7[0] = points[4];
    t7[1] = points[3];
    t7[2] = points[2];
    t7[3] = points[0];
    tets.push_back(t7);

    return tets;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<unsigned int> Pyramid::getTetra(int index)
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
        t[2] = points[3];
        t[3] = points[4];
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
        t[1] = points[3];
        t[2] = points[1];
        t[3] = points[4];
    }
    else if (index == 3)
    {
        t[0] = points[3];
        t[1] = points[0];
        t[2] = points[2];
        t[3] = points[4];
    }
    else if (index == 4)
    {
        t[0] = points[4];
        t[1] = points[0];
        t[2] = points[3];
        t[3] = points[1];
    }
    else if (index == 5)
    {
        t[0] = points[4];
        t[1] = points[1];
        t[2] = points[0];
        t[3] = points[2];
    }
    else if (index == 6)
    {
        t[0] = points[4];
        t[1] = points[2];
        t[2] = points[1];
        t[3] = points[3];
    }
    else if (index == 7)
    {
        t[0] = points[4];
        t[1] = points[3];
        t[2] = points[2];
        t[3] = points[0];
    }
    return t;
}

// memorist
vector<unsigned int> Pyramid::getFacePoints(const unsigned int &index)
{

    vector<unsigned int> aux;

    switch (index)
    {
    case 0:
        aux.reserve(4);
        aux.push_back(points[0]);
        aux.push_back(points[3]);
        aux.push_back(points[2]);
        aux.push_back(points[1]);
        break;
    case 1:
        aux.reserve(3);
        aux.push_back(points[0]);
        aux.push_back(points[1]);
        aux.push_back(points[4]);
        break;
    case 2:
        aux.reserve(3);
        aux.push_back(points[1]);
        aux.push_back(points[2]);
        aux.push_back(points[4]);
        break;
    case 3:
        aux.reserve(3);
        aux.push_back(points[2]);
        aux.push_back(points[3]);
        aux.push_back(points[4]);
        break;
    case 4:
        aux.reserve(3);
        aux.push_back(points[3]);
        aux.push_back(points[0]);
        aux.push_back(points[4]);
        break;
    default:
        break;
    }
    return aux;
}
//--
