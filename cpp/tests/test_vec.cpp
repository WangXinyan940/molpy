#include "vec.h"
#include <gtest/gtest.h>

TEST(testVec3, default_construct)
{
    Vec3<int> v;
    EXPECT_EQ(0, v.x);
    EXPECT_EQ(0, v.y);
    EXPECT_EQ(0, v.z);
}

TEST(testVec3, index)
{
    Vec3<int> v = {1,2,3};
    EXPECT_EQ(1, v[0]);
    EXPECT_EQ(2, v[1]);
    EXPECT_EQ(3, v[2]);
}