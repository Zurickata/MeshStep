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

#include "Element.h"

//---------------------------------------------------------------//
//---------------------------------------------------------------//
Element::Element()
{
    type = 'E';
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
Element::Element(vector<int> &pts)
{
    points.assign(pts.size(), 0);
    for (unsigned int i = 0; i < pts.size(); i++)
    {
        points[i] = pts[i];
    }
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
Element::~Element()
{
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Element::getEdgeAspectRatio(vector<Point3D> &points)
{
    cout << "not imeplemented\n";
    return 0;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//

// memorist
void Element::computeBbox(vector<Point3D> &coords)
{

    if (points.empty())
    {
        cerr << "element with no nodes created\n";
        return;
    }

    // the initial values of min and max correspond to the
    // coords of the first point.
    if (points[0] >= coords.size())
    {
        cout << "out of boundary: " << points[0] << "/" << coords.size() << endl;
        return;
    }
    min[0] = max[0] = coords.at(points[0])[0];
    min[1] = max[1] = coords.at(points[0])[1];
    min[2] = max[2] = coords.at(points[0])[2];

    for (unsigned int i = 1; i < points.size(); i++)
    {
        if (points[i] >= coords.size())
        {
            cout << "out of boundary: " << points[i] << "/" << coords.size() << endl;
            return;
        }
        double x = coords.at(points[i])[0];
        double y = coords.at(points[i])[1];
        double z = coords.at(points[i])[2];

        if (min[0] > x)
            min[0] = x;
        if (max[0] < x)
            max[0] = x;
        if (min[1] > y)
            min[1] = y;
        if (max[1] < y)
            max[1] = y;
        if (min[2] > z)
            min[2] = z;
        if (max[2] < z)
            max[2] = z;
    }
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
double Element::getElementJS(vector<Point3D> &pts)
{

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
double Element::getElementJENS(vector<Point3D> &pts)
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
double Element::getElementJEANS(vector<Point3D> &pts)
{

    // IMPORTANT NOTE: this method is redifined in class
    // Prism and Pyramid. For the case of Hexahedron is also
    // redefined for an optimization (its Jens constant is 1).
    // For default is computed as follows:

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
double Element::getElementJRATIO(vector<Point3D> &pts)
{

    double worst = 2;

    vector<double> jrs = getJRatios(pts);

    for (unsigned int i = 0; i < points.size(); i++)
    {
        if (jrs[i] < worst)
        {
            worst = jrs[i];
        }
    }

    return worst;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Element::getJS(vector<Point3D> &pts)
{

    vector<vector<unsigned int>> tets = getTetras();
    vector<double> js(tets.size(), 0);

    for (unsigned int i = 0; i < tets.size(); i++)
    {

        Point3D v0 = pts[tets[i][1]] - pts[tets[i][0]];
        Point3D v1 = pts[tets[i][2]] - pts[tets[i][0]];
        Point3D v2 = pts[tets[i][3]] - pts[tets[i][0]];

        v0.normalize();
        v1.normalize();
        v2.normalize();

        js[i] = (v0.cross(v1)).dot(v2);
    }

    return js;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Element::getJENS(vector<Point3D> &pts)
{

    // IMPORTANT NOTE: For the case of Hexahedron this method is
    // redefined for an optimization (its Jens constant is 1).

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

        jens[i] = q;
    }

    return jens;
}

//---------------------------------------------------------------//
//---------------------------------------------------------------//
vector<double> Element::getJEANS(vector<Point3D> &pts)
{

    // IMPORTANT NOTE: this method is redifined in class
    // Prism and Pyramid. For the case of Hexahedron is also
    // redefined for an optimization (its Jens constant is 1).
    // For default is computed as follows:

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

// memorist
void Element::remove(int axe, double start, double end)
{
    if (min[axe] < start || max[axe] > end)
        removed = true;
    else
        removed = false;
}
//--

//---------------------------------------------------------------//
//---------------------------------------------------------------//
std::ostream &operator<<(std::ostream &o, Element &e)
{
    vector<unsigned int> points = e.getPoints();
    o << e.getCharType();
    for (unsigned int i = 0; i < points.size(); i++)
    {
        o << " " << points[i];
    }
    return o;
}

/*void Element::printer(FaceContainer &fc, FaceContainer &sfc)
{
    list<unsigned int>::iterator iter;

    for (iter = faces.begin(); iter != faces.end(); iter++)
    {
        sfc.addFace(fc.getFace(*iter));
    }
}

void Element::ESChecker(FaceContainer &fc, FaceContainer &sfc)
{
    list<unsigned int>::iterator iter;
    list<unsigned int>::iterator iter2;
    for (iter = faces.begin(); iter != faces.end(); iter++)
    {
        if (fc.getFace(*iter).numberOfElements() == 1)
        {
            surfaceElement = true;
            // Element=true;
            for (iter2 = faces.begin(); iter2 != faces.end(); iter2++)
            {
                sfc.addFace(fc.getFace(*iter2));
            }
            break;
            // fc.getFace(*iter).setColor(color);
            // sfc.(fc.getFace(*iter));
        }
    }
}*/
//--